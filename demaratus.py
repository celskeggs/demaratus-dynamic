import webapp2, os, cgi, datetime, sys, time, logging, keyfile, json
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from google.appengine.api import channel, users
from google.appengine.ext import ndb

class DataBlock(ndb.Model):
	contents = ndb.BlobProperty(required=True)

aes_key = keyfile.aes_key
def digest(x):
	digest = SHA256.new()
	digest.update(x)
	out = digest.digest()
	assert len(out) == 32
	return out
def digest_hex(x):
	return digest(x).encode("hex")
def verified(x):
	if not x:
		return None
	d = digest(x)
#	logging.info("A: '%s', '%s'" % (d, x))
	return d + x
def verify(x):
	if not x:
		return None
	hsh = x[:32]
	data = x[32:]
#	logging.info("A: '%s', '%s'" % (hsh, data))
	if digest(data) != hsh:
		logging.warning("Malformed data - failed verification")
		return None
	return data
def encode(x):
	if not x:
		return None
	iv = Random.new().read(16)
	cipher = AES.new(aes_key, AES.MODE_CFB, iv)
	msg = iv + cipher.encrypt(x)
	return msg
def decode(msg):
	if not msg:
		return None
	iv = msg[:16]
	if len(iv) != 16:
		logging.warning("Malformed data - failed iv check")
		return None
	enc = msg[16:]
	cipher = AES.new(aes_key, AES.MODE_CFB, iv)
	return cipher.decrypt(enc)
def encode_verified(x):
	return encode(verified(x))
def verify_decode(x):
	return verify(decode(x))
def get_data(keyraw, default=None):
	if not keyraw:
		return default
	key = ndb.Key(DataBlock, keyraw)
	blk = key.get()
	if not blk:
		return default
	data = blk.contents
	assert digest_hex(data) == keyraw, "Bad stored data - bad hash"
	return verify_decode(data)
def put_data(data):
	data = encode_verified(data)
	keyraw = digest_hex(data)
	key = ndb.Key(DataBlock, keyraw)
	blk = DataBlock(key=key, contents=data)
	return blk.put()

class TestPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/plain"
		self.response.write("{0A2B-DF8C}\n")
		for sample in DataBlock.query().fetch(20):
			self.response.write("Sample: %s = %s\n" % (sample.key, sample.contents.encode("hex")))
#class EditPage(webapp2.RequestHandler):
#	def get(self):
#		self.response.headers["Content-Type"] = "text/html"
#		basedata = (get_data(self.request.get("base")) or "Write your text here!").decode()
#		self.response.write("""""".replace("{contents}",json.dumps(basedata)))
class TestPage2(webapp2.RequestHandler):
	def get(self):
		if self.request.get("list"):
			self.response.headers["Content-Type"] = "application/json"
			self.response.write(json.dumps([x.id() for x in DataBlock.query().fetch(keys_only=True)]))
		else:
			data = get_data(self.request.get("key"))
			if data:
				if self.request.get("hex", "false").lower() == "true":
					self.response.headers["Content-Type"] = "text/plain"
					self.response.write(data.encode("hex"))
				else:
					self.response.headers["Content-Type"] = "application/octet-stream"
					self.response.write(data)
			else:
				webapp2.abort(404)
	def post(self):
		self.response.headers["Content-Type"] = "text/plain"
		data = self.request.get("data")
		if data:
			data = data.encode()
			if self.request.get("hex", "false").lower() == "true":
				data = data.encode("hex")
			key = put_data(data)
			self.response.write("%s\n" % key)
		else:
			webapp2.abort(404)

application = webapp2.WSGIApplication([
	('/', TestPage),
	('/data', TestPage2),
#	('/edit', EditPage)
])
#sdkfetch = webapp2.WSGIApplication([
#	
#])
# before the other entry:
#- url: /_ah/.*
#  script: demaratus.skdfetch
#  secure: always
#  login: admin
