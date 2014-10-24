import urllib, urllib2, requests
from binascii import hexlify, unhexlify

def returnHex(num):
    return "%02x" % num

def xorStrings(s1, s2):
    return hexlify(''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(unhexlify(s1[-len(s2):]), unhexlify(s2))))

def getCT():
    url = 'http://localhost:8080/eavesdrop'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    x = response.read()
    return x.split('<p><font color="red"> ')[1].split(' </font>')[0]

def queryWebsite():
    cipherTxt = getCT()
    url = 'http://localhost:8080/'
    answer = []
    index = len(cipherTxt) - 1
    tempCT = list(cipherTxt)
    x = 1 
    while index > 0:
        guessTxt = list(cipherTxt)
        for count in range(0x00, 0xff):
            val = returnHex(count)
            print(val)
            print(index)
            guessTxt[index - 1] = val[0]
            guessTxt[index] = val[1]
            values = {'enc': "".join(guessTxt)}
            r = requests.get('http://localhost:8080/', params=values)
            if r.status_code == 404:
                tempVal = int(tempCT[index -1] + tempCT[index], 16)
                answer.append(returnHex(int(val, 16) ^ tempVal))
        index -= 2
    print(answer)
queryWebsite()
