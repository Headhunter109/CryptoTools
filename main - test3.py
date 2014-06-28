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
form2="""<center><h2>Enter Cipher text to Decrypt Using Rail Fence</h2><p>Note:- Ciphertext should be encrypted using Rail Fence</p><form method="post">
<textarea input type="text" name="ciphertext">%(ciphertext)s</textarea><br/>
<input type="submit">
<p>%(plaintext)s</p>
</form>

<div style="text-align:center;padding-top:50px;color:red"><p>&copy; Chetan Khatri</p></div></center></center> """
vform="""<center><h2>Enter Text to Encrypt Using Vegenere Cipher</h2>
<form method="post">
<textarea input type="text" name="ciphertext">%(ciphertext)s</textarea><br/>
<input type="text" name="key" value="%(key)s"/><br/>
<input type="submit">
<p>%(plaintext)s</p>
</form>

<div style="text-align:center;padding-top:50px;color:red"><p>&copy; Chetan Khatri</p></div></center></center>  """
#Attack Rail fence starts here
def offset(even, rails, rail):
    if rail == 0 or rail == rails - 1:
        return (rails - 1) * 2

    if even:
        return 2 * rail
    else:
        return 2*(rails - 1 - rail)



def decryptRailFence(encrypted, rails, showOff = 0):
    array = [[" " for col in range(len(encrypted))] for row in range(rails)]
    read = 0
    
    #build our fence
    for rail in range(rails):
        pos = offset(1, rails, rail)
        even = 0;
        
        if rail == 0:
            pos = 0
        else:
            pos = int(pos / 2)
        
        while pos < len(encrypted):
            if read == len(encrypted):
                break

            array[rail][pos] = encrypted[read];
            read = read + 1

            pos = pos + offset(even, rails, rail)
            even = not even


    if showOff:
        #Output work
        for row in array:
            print (row)

    #now return the decoded message
    decoded = ""

    for x in range(len(encrypted)):
        for y in range(rails):
            if array[y][x] != " ":
                decoded += array[y][x]

    return decoded

#Attack Rail fence Ends here

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
class AttackRailHandler(webapp2.RequestHandler):
     def post(self):
        self.response.write(form2)
     def write_form(self,plaintext = '',ciphertext=''):
        self.response.write(form2 % {'plaintext':plaintext,'ciphertext': ciphertext})
        
     def get(self):
        self.write_form()

     def post(self):
         content='';
         for i in range(10):
             content=content + (decryptRailFence(self.request.get('ciphertext'), i	, 0)) +'<br/>'

         self.write_form(content,self.request.get('ciphertext'))

app = webapp2.WSGIApplication([
     ('/', MainHandler),('/railfence',RailHandler),('/attackrailfence',AttackRailHandler),('/vegenere',Vegenere
    ], debug=True)
