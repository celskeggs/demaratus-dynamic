import webapp2, os, cgi, datetime, sys, time, logging
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from google.appengine.api import channel, users
from google.appengine.ext import ndb

class DataBlock(ndb.Model):
	contents = ndb.TextProperty(required=True)

def digest(x):
	digest = SHA256.new()
	digest.update(x)
	out = digest.digest().encode("hex")
	assert len(out) == 64
	return out
def get_data(keyraw):
	key = ndb.Key(DataBlock, keyraw)
	blk = key.get()
	data = blk.contents
	assert digest(data) == keyraw, "Bad stored data - bad hash"
	return data
def put_data(data):
	keyraw = digest(data)
	key = ndb.Key(DataBlock, keyraw)
	blk = DataBlock(key=key, contents=contents)
	return blk.put()

class TestPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/plain"
		self.response.write("{0A2B-DF8C}\n")
		for sample in DataBlock.query().fetch(20):
			self.response.write("Sample: %s = %s" % (sample.key, sample.contents))
class EditPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/html"
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
</script>
</body>
</html>""".replace("{contents}",cgi.escape("<div>")))
class TestPage2(webapp2.RequestHandler):
	def post(self):
		self.response.headers["Content-Type"] = "text/plain"
		contents = self.request.get("data")
		digest = SHA256.new()
		digest.update(contents)
		keyraw = digest.digest().encode("hex")
		assert len(keyraw) == 64
		key = ndb.Key(DataBlock, keyraw)
		if not key or not contents:
			self.response.write("Missing\n")
		else:
			blk = DataBlock(key=key, contents=contents)
			self.response.write("Out: %s\n" % blk.put())

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
