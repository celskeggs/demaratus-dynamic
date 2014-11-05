import webapp2, os, cgi, datetime, sys, time, logging, keyfile
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from google.appengine.api import channel, users
from google.appengine.ext import ndb

class DataBlock(ndb.Model):
	contents = ndb.TextProperty(required=True)

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
	return data
def put_data(data):
	keyraw = digest_hex(data)
	key = ndb.Key(DataBlock, keyraw)
	blk = DataBlock(key=key, contents=data)
	return blk.put()

class TestPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/plain"
		self.response.write("{0A2B-DF8C}\n")
		for sample in DataBlock.query().fetch(20):
			self.response.write("Sample: %s = %s\n" % (sample.key, sample.contents))
class EditPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/html"
		basedata = (verify_decode(get_data(self.request.get("base"))) or "Write your text here!").decode()
		self.response.write("""<!DOCTYPE html>
<html lang="en">
<head>
<title>Demaratus Editor</title>
<style type="text/css" media="screen">
	#editor { 
		position: absolute;
		top: 0;
		right: 20%;
		bottom: 0;
		left: 0;
	}
	#sidebar {
		position: absolute;
		top: 0;
		bottom: 0;
		left: 80%;
		right: 0;
		background-color: #2f3129;
		color: #8f908a;
		font: 20px "Monaco","Menlo","Ubuntu Mono","Consolas","source-code-pro",monospace;
	}
	#submit {
		position: absolute;
		left: 0;
		right: 0;
		margin: auto;
		top: 20%;
		width: 200px;
		height: 100px;
		background-color: #2f7a29;
		border: none;
		border-radius: 30px;
		color: #FFFFFF;
		font: 40px "Monaco","Menlo","Ubuntu Mono","Consolas","source-code-pro",monospace;
	}
</style>
<script type="text/javascript" src="/static/sjcl.js"></script>
</head>
<body>

<div id="editor">{contents}</div>
<div id="sidebar">
  <form method="post" action="/add" id="sidebar-form">
    <button id="submit">SUBMIT</button>
	<input id="sidebar-data" name="data" value="" type="hidden" />
  </form>
</div>
    
<script src="/static/ace/ace.js" type="text/javascript" charset="utf-8"></script>
<script>
	var editor = ace.edit("editor");
	editor.setTheme("ace/theme/monokai");
	// editor.getSession().setMode("ace/mode/javascript");
	function do_submit() {
		document.getElementById("sidebar-data").value = editor.getValue();
		document.getElementById("sidebar-form").submit();
	}
	document.getElementById("submit").onclick = do_submit;
	var ciphertext = sjcl.encrypt("password", "Hello World!")
	var plaintext = sjcl.decrypt("password", ciphertext)

	console.log(ciphertext)
	console.log(plaintext)
</script>
</body>
</html>""".replace("{contents}",cgi.escape(basedata)))
class TestPage2(webapp2.RequestHandler):
	def post(self):
		self.response.headers["Content-Type"] = "text/plain"
		contents = self.request.get("data")
		if contents:
			key = put_data(encode_verified(contents.encode()))
			self.response.write("Out: %s\n" % key)
		else:
			self.response.write("Missing\n")

application = webapp2.WSGIApplication([
	('/', TestPage),
	('/add', TestPage2),
	('/edit', EditPage)
])
#sdkfetch = webapp2.WSGIApplication([
#	
#])
# before the other entry:
#- url: /_ah/.*
#  script: demaratus.skdfetch
#  secure: always
#  login: admin
