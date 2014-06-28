import webapp2
import cgi
form="""<center>
<form method="post">
<input type="Submit" name="btnRot13" value="ROT 13"/>
<input type="Submit" name="btnRailFence" value="Rail Fence"/>
<input type="Submit" name="btnCrackRail" value="Crack Rail Fence"/>
<input type="Submit" name="btnVigenere" value="Vigenere"/>
<h2>Enter Some text here to Encrypt Using ROT13</h2><br/>
<textarea input type="text" name="plaintext">%(plaintext)s</textarea><br/>
<input type="submit"/>
</form><div style="text-align:center;padding-top:50px;color:red"><p>&copy; Chetan Khatri</p></div></center></center>"""
form1=""" <center><form method="post" style="padding-top:30px">
	
	<input type="Submit" name="btnRot13" value="ROT 13"/>
	<input type="Submit" name="btnRailFence" value="Rail Fence"/>
	<input type="Submit" name="btnCrackRail" value="Crack Rail Fence"/>
	<input type="Submit" name="btnVigenere" value="Vigenere"/>
	<br/>
	<h2>Rail fence Cipher</h2>
	<br/>
	<h2>Plaintext</h2>
	<textarea input type="text" name="plaintext">%(plaintext)s</textarea><br/>
	<p>Enter Key</p>
	<input type="text" name="key" value="%(key)s"/>
	<h2>Ciphertext</h2>
	<textarea input type="text" name="ciphertext">%(ciphertext)s</textarea><br/>
	<input type="Submit" name="encrypt" value="Encrypt"/>
	<br/><div style="text-align:center;padding-top:50px;color:red"><p>&copy; Chetan Khatri</p></div></center>
</form> """
form2="""<center><form method="post">
<input type="Submit" name="btnRot13" value="ROT 13"/>
	<input type="Submit" name="btnRailFence" value="Rail Fence"/>
	<input type="Submit" name="btnCrackRail" value="Crack Rail Fence"/>
	<input type="Submit" name="btnVigenere" value="Vigenere"/>
	<br/>
	<h2>Enter Cipher text to Decrypt Using Rail Fence</h2><p>Note:- Ciphertext should be encrypted using Rail Fence</p>
<textarea input type="text" name="ciphertext">%(ciphertext)s</textarea><br/>
<input type="submit">
<p>%(plaintext)s</p>
</form>

<div style="text-align:center;padding-top:50px;color:red"><p>&copy; Chetan Khatri</p></div></center></center> """
vform="""<center>
<form method="post">
<input type="Submit" name="btnRot13" value="ROT 13"/>
<input type="Submit" name="btnRailFence" value="Rail Fence"/>
<input type="Submit" name="btnCrackRail" value="Crack Rail Fence"/>
<input type="Submit" name="btnVigenere" value="Vigenere"/>
<br/>
<h2>Enter Text to Encrypt Using Vigenere Cipher</h2><br/>
<textarea input type="text" name="plaintext">%(plaintext)s</textarea><br/>
<input type="text" name="key" value="%(key)s"/><br/>
<input type="submit"><br/><br/>
<h3>Cipher Text:</h3>
<p>%(ciphertext)s</p>

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

#Encryption Vegenere Starts
key_len=0
def vege(msg,key):
	global key_len
	cipher=[]
	
	for i in range(len(msg)):
		 key_len=len(key)
		 
		 cipher.append(caesar(ord(msg[i]),ord(key[i])))
		 if(len(msg) > i):
		     key=key+str(key[i])
		 
	return ''.join(cipher)

def caesar(token,key):
	
	return chr(((((token - 65)  +(key+65))%26)+65))

#Encryption Vegenere Ends

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
         rot13s=self.request.get('btnRot13')
         RailFence=self.request.get('btnRailFence')
         CrackRail=self.request.get('btnCrackRail')
         Vige=self.request.get('btnVigenere')
         
         if rot13s:
             self.redirect('/')
         elif RailFence:
             self.redirect('/railfence')
         elif CrackRail:
             self.redirect('/attackrailfence')
         elif Vige:
             self.redirect('/vigenere')
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
        rot13s=self.request.get('btnRot13')
        RailFence=self.request.get('btnRailFence')
        CrackRail=self.request.get('btnCrackRail')
        Vige=self.request.get('btnVigenere')
         
        if rot13s:
             self.redirect('/')
        elif RailFence:
             self.redirect('/railfence')
        elif CrackRail:
             self.redirect('/attackrailfence')
        elif Vige:
             self.redirect('/vigenere')
        plaintext=self.request.get('plaintext')
        key=self.request.get('key')
        if plaintext!='' and key!='':
             content = encrypt(plaintext,int(key))
             self.write_form(plaintext,content,key)
        else:
             self.write_form('Enter Plaintext','','Enter Key')
class VegHandler(webapp2.RequestHandler):
     key_len=0 
     def post(self):
        self.response.write(vform)
     def write_form(self, plaintext = '', ciphertext='',key=''):
        self.response.write(vform % {'plaintext': plaintext,'ciphertext':ciphertext,'key':key})
        
     def get(self):
        self.write_form()

     def post(self):
        rot13s=self.request.get('btnRot13')
        RailFence=self.request.get('btnRailFence')
        CrackRail=self.request.get('btnCrackRail')
        Vige=self.request.get('btnVigenere')
         
        if rot13s:
             self.redirect('/')
        elif RailFence:
             self.redirect('/railfence')
        elif CrackRail:
             self.redirect('/attackrailfence')
        elif Vige:
             self.redirect('/vigenere')
        global key_len
        msg=self.request.get('plaintext')
        key=self.request.get('key')
        if (msg.isalpha() and key.isalpha()):
             key_len=len(key)
             cipher=vege(msg,key)
             self.write_form(msg,cipher,key)
        else:
             self.write_form(msg,'Key and Message Should be Alphabetic',key)
             
        
class AttackRailHandler(webapp2.RequestHandler):
     def post(self):
        self.response.write(form2)
     def write_form(self,plaintext = '',ciphertext=''):
        self.response.write(form2 % {'plaintext':plaintext,'ciphertext': ciphertext})
        
     def get(self):
        self.write_form()

     def post(self):
        rot13s=self.request.get('btnRot13')
        RailFence=self.request.get('btnRailFence')
        CrackRail=self.request.get('btnCrackRail')
        Vige=self.request.get('btnVigenere')
         
        if rot13s:
             self.redirect('/')
        elif RailFence:
             self.redirect('/railfence')
        elif CrackRail:
             self.redirect('/attackrailfence')
        elif Vige:
             self.redirect('/vigenere')
        content='';
        for i in range(10):
             content=content + (decryptRailFence(self.request.get('ciphertext'), i	, 0)) +'<br/>'

        self.write_form(content,self.request.get('ciphertext'))

app = webapp2.WSGIApplication([
     ('/', MainHandler),('/railfence',RailHandler),('/attackrailfence',AttackRailHandler),('/vigenere',VegHandler)
    ], debug=True)
