#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
form="""<center><h2>Enter Some text here to Encrypt Using ROT13</h2><br/><form method="post">
<textarea input type="text" name="plaintext">%(plaintext)s</textarea><br/>
<input type="submit">
</form><div style="text-align:center;padding-top:50px;color:red"><p>&copy; Chetan Khatri</p></div></center></center>"""
form1=""" <center><h2>Rail fence Cipher</h2><form method="post" style="padding-top:30px">
	<h2>Plaintext</h2>
	<textarea input type="text" name="plaintext">%(plaintext)s</textarea><br/>
	<p>Enter Key</p>
	<input type="text" name="key" value="%(key)s"/>
	<h2>Ciphertext</h2>
	<textarea input type="text" name="ciphertext">%(ciphertext)s</textarea><br/>
	<input type="Submit" name="encrypt" value="Encrypt"/>
	<br/><div style="text-align:center;padding-top:50px;color:red"><p>&copy; Chetan Khatri</p></div></center>
</form> """

def rot13(s):
	return "".join([chr((ord(i) - 65 + 13) % 26 + 65)
				for i in s.upper()
				if ord(i) >= 65 and ord(i) <= 90 ])
def escape_html(s):
        return cgi.escape(s, quote = True)
def encrypt(msg, n):
    cipher = ""
    n=n+1
    for i in range(n):
        for j in range(i, len(msg), n):
            cipher = cipher + msg[j]
            #print(cipher)
    return cipher

class MainHandler(webapp2.RequestHandler):
    def post(self):
        self.response.write(form)

    def write_form(self,plaintext=""):
         self.response.write(form % {"plaintext" : escape_html(plaintext)})
    def get(self):
         self.write_form()
    def post(self):
         stringtoconvert = self.request.get('plaintext')
         convertedstring = rot13(stringtoconvert)
         self.write_form(convertedstring)
class RailHandler(webapp2.RequestHandler):
     def post(self):
        self.response.write(form1)
     def write_form(self, plaintext = '', ciphertext='',key=''):
        self.response.write(form1 % {'plaintext': plaintext,'ciphertext':ciphertext,'key':key})
        
     def get(self):
        self.write_form()

     def post(self):
        content = encrypt(self.request.get('plaintext'),int(self.request.get('key')))
        self.write_form(self.request.get('plaintext'),content,self.request.get('key'))
    
app = webapp2.WSGIApplication([
     ('/', MainHandler),('/railfence',RailHandler)
    ], debug=True)
