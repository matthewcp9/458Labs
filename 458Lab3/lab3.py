import urllib, urllib2, requests, struct, base64, os, hashlib, sys, datetime
from binascii import hexlify, unhexlify

# Task 1 -------

def paddingOracle():
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
        url = 'http://127.0.0.1:8080'
        answer = []
        block = 1
        text = ""

        print(cipherTxt)
        print(len(cipherTxt)//32);
        length = len(cipherTxt)//32
        while(block < len(cipherTxt)//32):
            plaintext = [-1] * 16
            c2 = cipherTxt[(length - block) * 32 : (length - block + 1) * 32]
            c1r = cipherTxt[(length - block - 1) * 32 : (length - block) * 32]
            c1 = list("00000000000000000000000000000000")
            for index in range(0, 16):
                print(index)
                for ptl in range(16 - index, 16):
                    temp = returnHex(plaintext[ptl] ^ (index + 1) ^ int(c1r[ptl * 2 : ptl * 2 + 2], 16))
                    c1[ptl * 2] = temp[0]
                    c1[ptl * 2 + 1] = temp[1]
                    #print(c1, "Plaintext: ", plaintext[ptl], index, ptl, c1r[ptl * 2 : ptl * 2 + 2])
                for count in range(0x00, 256):
                    #print(count)
                    val = returnHex(count)
                    c1[31 - (index * 2) - 1] = val[0]
                    c1[31 - index * 2] = val[1]
                    values = {'enc': ("".join(c1) + c2)}
                    #print(values)
                    req = requests.get('http://127.0.0.1:8080', params=values)
                    if req.status_code == 404:
                        print("Hello")
                        c1real = cipherTxt[(length - block - 1) * 32 : (length - block) * 32]
                        c1realv = c1real[31 - (index * 2) - 1 : 31 - (index * 2) + 1]
                        #print(val, c1real, c1realv)
                        plaintext[16 - index - 1] = int(val, 16) ^ (index + 1) ^ int(c1realv, 16)
                        count = 257
            print(plaintext)

            answer.append(plaintext)
            block += 1
        text = []
        answer = reversed(answer)
        for block in answer:
            for letter in block:
                text.append(chr(letter))
        print("".join(text))
        print(answer)
    queryWebsite()


#paddingOracle()

#10101101110111101001110001001010011010010010010001

# ---- Task 2

def SHA1(msg):
    def left_rotate(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xffffffff
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # message length in bits
    ml = len(msg) * 8
    #append the bit 'l' to the msg
    msg += chr(128)
    while (len(msg) + 8) % 64 != 0:
        msg += chr(0)
    #append ml, in a 64-bit big-endian integer.
    msg += struct.pack(b'>Q', ml)
    chunks = [msg[i:i+64] for i in range(0, len(msg), 64)]
    for chunk in chunks:
        # Break chunk into sixteen 32-bit big-endian words w[i]
        w = [0] * 80
        for i in range(16):
            w[i] = struct.unpack(b'>I', chunk[(i*4):(i*4 + 4)])[0]
        # Extend the sixteen 32-bit words into eighty 32-bit words:
        for i in range(16, 80):
            w[i] = left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(0, 80):
            if 0 <= i <= 19:
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            temp = left_rotate(a, 5) + f + e + k + w[i] & 0xffffffff
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp
        #have to mask with this
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
    hh = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    return "%x" % hh
#print(SHA1("abc") == 'a9993e364706816aba3e25717850c26c9cd0d89d')
#print(SHA1("The quick brown fox jumps over the lazy cog") == 'de9f2c7fd25e1b3afad3e85a0bd17d9b100db4b3')
#print(SHA1())

#Collisions
#72349653 
#23612730
def collisionSHA1():
    hashDict = {}
    used = {}
    mask = 0x3ffffffffffff
    x = 1
    total = 10000000

        
    while True:
        print(x)
        result = SHA1(str(x))
        lsbResult = int(result,16) & mask
        #print("%02x" % lsbResult)
        if lsbResult in hashDict:
            print("Found it")
            print(x)
            print(hashDict[lsbResult])
            break;
        hashDict[lsbResult] = x
        x += 1
    
#collisionSHA1()

# Task 3-----

def SHA1LE(msg, aa, bb, cc, dd, ee):
    def left_rotate(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xffffffff
    h0 = aa
    h1 = bb
    h2 = cc
    h3 = dd
    h4 = ee

    chunks = [msg[i:i+64] for i in range(0, len(msg), 64)]
    for chunk in chunks:
        # Break chunk into sixteen 32-bit big-endian words w[i]
        w = [0] * 80
        for i in range(16):
            w[i] = struct.unpack(b'>I', chunk[(i*4):(i*4 + 4)])[0]
        # Extend the sixteen 32-bit words into eighty 32-bit words:
        for i in range(16, 80):
            w[i] = left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(0, 80):
            if 0 <= i <= 19:
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            temp = left_rotate(a, 5) + f + e + k + w[i] & 0xffffffff
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp
        #have to mask with this
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
    hh = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    return "%x" % hh

def generatePadding(msgLen):
    msg = ""
    #rint("MSG", msgLen)
    ml = msgLen * 8
    msg += chr(128)
    msgLen += 1
    while (msgLen + 8) % 64 != 0:
        msg += chr(0)
        msgLen += 1
    msg += struct.pack(b'>Q', ml)
    return msg

def lengthExtendSha1():
    #values = {'who': ("Abbot"), 'what': ("Hello")}
    req = requests.get('http://localhost:8080/')
    html = req.text;

    
    who = str(html.split('<b><font color="white">')[1].split(' says:</font></b>')[0].strip())
    what = str(html.split("<div id='postContainer'>")[1].split(' </div>')[0].strip())
    mac = str(html.split("<div id='postFooter'>")[1].split(' </div>')[0].strip())

    addmsg = "Such as yours. fool"
    for keylen in range(1, 65):
        newMsg = what + generatePadding(len(what) + keylen) + addmsg
        lenOfOldMsg = len(what) + keylen + len(generatePadding(len(what) + keylen)) # guessed key length + original mesage length + the padding of the msg (the msg is key || orig msg)
        paddedMsg = addmsg + generatePadding(lenOfOldMsg + len(addmsg)) #Use that length and the length of your new msg to generate the padding for the new msg

        a = int(mac[0:8], 16)
        b = int(mac[8:16], 16)
        c = int(mac[16:24], 16)
        d = int(mac[24:32], 16)
        e = int(mac[32:40], 16)
        newMac = SHA1LE(paddedMsg, a, b, c, d, e)
        values = {'who': who, 'what': newMsg, 'mac': newMac}
        req = requests.get('http://localhost:8080/', params=values);
#lengthExtendSha1();

def HMAC(key, msg):
    blocksize = 64 #SHA1 implementation
    if len(key) > blocksize:
        key = SHA1(key)
    if len(key) < blocksize:
        key = key + ( 0x00 * (blocksize - len(key)))
    
    o_key_pad = [0x5c * blocksize] ^ key
    i_key_pad = [0x36 * blocksize] ^ key

    return SHA1(o_key_pad + SHA1(i_key_pad + msg))


# Task 4 ------

def constantTimeCompare(message, message_new):
    value = 0
    for x, y in zip(message, message_new):
        value |= ord(x) ^ ord(y)
    return value == 0

def timingAttack():
    while True: #basically if it messes up and doesn't find the correct solution... you gotta try again...
        solution = chr(47) * 20
        user = "foo"
        tries = 0
        timeElapsed = datetime.timedelta(microseconds=0)
        #finding the delay in compare
        for x in range(0, 20):
            
            times = {}
            maxChar = 0
            for i in range(0, 256):
                d = datetime.timedelta(microseconds=0)
                tempStr = list(solution)
                tempStr[x] = chr(i)
                solution = "".join(tempStr)
                testString = base64.b16encode(solution).lower()
                #print("Hello", testString)
                values = {'q' : 'foo', 'mac': testString}
                r = requests.get("http://127.0.0.1:8080", params=values)
                d += r.elapsed
                times[i] = d
            #print(times)
            if ((times[(max(times, key=times.get))] - timeElapsed) < datetime.timedelta(microseconds=4500)):
                x -= 2 #try the last byte again since it doesnt match up with the paused time delay 
                print("Time doesn't match up -- Going back to byte", x + 1)
            else:    
                timeElapsed += times[(max(times, key=times.get))]
                tempStr = list(solution)
                tempStr[x] = chr(max(times, key=times.get))
                solution = "".join(tempStr)
                print("Found so far ", x, "bytes")

    #print(solution)
        solution = base64.b16encode(solution).lower()
        values = {'q':user, 'mac':solution}
        r = requests.get("http://127.0.0.1:8080", params = values)
        if not 'Invalid' in r.text:
            print(r.text, x)
            break;
timingAttack()
def bForceLastBit():
    t = "0A35E0C5F92459551BBD92C868768A63E41E0A86".lower()
    #7F5D6D5BCB2A6C1B2EC7103E5D3E7B385FAABF40
    #D4894DA93AA6B4CA01D8840FF3CA6ECEA5FBF711
    for x in range(0, 256):
        temp = t + ("%02x" % x)
        #print(temp)
        values = {'q':"foo", 'mac':temp}
        r = requests.get("http://127.0.0.1:8080", params = values)
        if not 'Invalid' in r.text:
            print(r.text, x)
#bForceLastBit()