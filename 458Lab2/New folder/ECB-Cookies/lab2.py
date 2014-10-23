from Crypto.Cipher import AES, XOR
from Crypto import Random
import urllib
import urllib2
import cookielib
import base64
import binascii

global jar

def str2bin(string):    
    return ' '.join([bin(ord(x))[2:] for x in string])

def str2hex(string):    
    return ' '.join([('%02X' % ord(x)) for x in string])

def pad(blockSize, message):
    #message = str2hex(message)
    msgSize = len(message)
    diff = blockSize - msgSize
    lmk = msgSize % blockSize
    lmk = blockSize - lmk;
    
    if diff > 0:
        b = []
        for x in range(0, diff):
            b.append(chr(diff))
        message += ''.join(b)
    return message


def unpad(blockSize, padmsg):
    msgLength = len(padmsg)
    
    paddedBytes = ord(padmsg[-1])
    if paddedBytes > (blockSize):
        return "Too many bytes were padded on %d" % paddedBytes
    
    for x in range(0, paddedBytes):
        if ord(padmsg[-1]) != paddedBytes:
            return ("Invalid bytes at %d got %d expected %d" % (x,ord(padmsg[-1]), paddedBytes))
        padmsg = padmsg[:-1]
    return padmsg

x = pad(20, 'bbbxx')

def ecb_encrypt(pt, key):
    cipher = AES.new(key, AES.MODE_ECB)
    pt = pad(128, pt)
    return cipher.encrypt(pt)

def ecb_decrypt(ct, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(16, cipher.decrypt(ct))

def Task2A():
    with open("Lab2.TaskII.A.txt", "rb") as file:
        print(ecb_decrypt(base64.b64decode(file.read()), "CALIFORNIA LOVE!"))

def Task2B():    
    with open("Lab2.TaskII.B.txt", "rb") as file:
        dict1 = {}
        for line in file:
            count = 0
            dict2 = {}
            temp = line.strip().decode('hex')
            while len(temp) >= 16:
                extracted = temp[:16]
                if extracted in dict2:
                    count += 1
                else:
                    dict2[extracted] = "found"
                temp = temp[16:]
            dict1[line] = count
        
    with open("result.bmp", "wb") as outfile:
        outfile.write(max(dict1, key=dict1.get).strip().decode('hex'))
        outfile.close()

def registerAccount(user, password):
    url = 'http://localhost:8080/register'
    values = {'user': user, 'password': password}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)

def loginUser(user, password):
    global jar
    jar = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(jar)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    
    url = 'http://localhost:8080'
    values = {'user': user, 'password': password}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    for cookie in jar:
        return str(cookie)[19:-22]
       

def Task2C():  
    charUser= "12345678912" + "admin" + (chr(0) * 10) + chr(11)
    password = '123'
    registerAccount(charUser, password)
    cookie = loginUser(charUser, password)
    print(cookie)
    adminKey = cookie[32:64]
    print(adminKey)

    charUser= "abcdefghijk" + "admin" + (chr(0) * 10) + chr(11)
    password = '123'
    registerAccount(charUser, password)
    cookie = loginUser(charUser, password)
    print(cookie)
    #adminKey = cookie[32:64]

    charUser2 = "matthewtrin" + "h123"
    password = '123'
    registerAccount(charUser2, password)
    cookie2 = loginUser(charUser2, password)
    print(cookie2)
    cookie2 = cookie2[0:len(cookie2) - 32] + adminKey
    print(cookie2)

def cbc_encrypt(pt, key, iv):
    blocksize = AES.block_size
    aes_obj = AES.new(bytes(key))
    pt = pad(blocksize, pt)
    
    ct = ""
    for x in range(0, len(ct) // blocksize - 1):
        ptblock = ct[x * blocksize:(x+1) * blocksize]
        pt_xor_iv = "".join([chr(ord(a) ^ ord(b)) for (a,b) in zip(pt, iv)])
        aes_obj.encrypt(pt_xor_iv)
        ct += pt_xor_iv
        iv = pt_xor_iv
    padblock = pad(blocksize, ct[(len(ct) - 1) * blocksize: len(ct)])
    pt_xor_iv = "".join([chr(ord(a) ^ ord(b)) for (a,b) in zip(pt, iv)])
    aes_obj.encrypt(pt_xor_iv)
    ct += pt_xor_iv
    return ct

def cbc_decrypt(ct, key, iv):
    blocksize = AES.block_size
    aes_obj = AES.new(bytes(key))
    msg = ""
    ct = ct.strip()
    print(len(ct.strip()))
    if len(ct) % blocksize > 0:
        return "Error, CipherText not multiple of Block Size"
       
    for x in range(0, len(ct) // blocksize):
        ctblock = ct[x * blocksize:(x+1) * blocksize]
        decrypted = aes_obj.decrypt(ctblock)
        msg += "".join([chr(ord(a) ^ ord(b)) for (a,b) in zip(decrypted, iv)])
        iv = ctblock       
    return unpad(blocksize, msg)

def Task3A():
    with open("Lab2.TaskIII.A.txt", "rb") as file:
        x = base64.b64decode(file.read())
        print(cbc_decrypt(x, "MIND ON MY MONEY", "MONEY ON MY MIND"))

def Task3B():
    charUser = "matthew1234"  + "0000000000000000" + "1role2admin11111"  + "1111111111"
    password = '123'
    attack_str = "&uid=3AAAAAAAAAA"
    attack_str2 = "&role=admin"
    registerAccount(charUser, password)
    cookie = loginUser(charUser, password)
    x = list(cookie)
    cookie = "".join(x)
    print(cookie)

    num = int(cookie[26:26 + 2], 16)
    temp = "%02x" % (num ^ (ord("2") ^ ord("&")))
    x[26] = temp[0]
    x[26 + 1] = temp[1]

    num = int(cookie[28:28 + 2], 16)
    temp = "%02x" % (num ^ (ord("3") ^ ord("x")))
    x[28] = temp[0]
    x[28 + 1] = temp[1]
    
    num = int(cookie[30:30 + 2], 16)
    temp = "%02x" % (num ^ (ord("4") ^ ord("=")))
    x[30] = temp[0]
    x[30 + 1] = temp[1]

    num = int(cookie[64:64 + 2], 16)
    temp = "%02x" % (num ^ (ord("1") ^ ord("&")))
    x[64] = temp[0]
    x[64 + 1] = temp[1]
    
    num = int(cookie[74:74 + 2], 16)
    temp = "%02x" % (num ^ (ord("2") ^ ord("=")))
    x[74] = temp[0]
    x[74 + 1] = temp[1]

    num = int(cookie[86:86 + 2], 16)
    temp = "%02x" % (num ^ (ord("1") ^ ord("&")))
    x[86] = temp[0]
    x[86 + 1] = temp[1]

    cookie = "".join(x)
    print(cookie)

    """
    num = int(cookie[138:138 + 2], 16)
    temp = "%02x" % (num ^ (ord("u") ^ ord("a")))
    x[138 + 0] = temp[0]
    x[138 + 1] = temp[1]

    num = int(cookie[140:140 + 2], 16)
    temp = "%02x" % (num ^ (ord("s") ^ ord("d")))
    x[140 + 0] = temp[0]
    x[140 + 1] = temp[1]

    num = int(cookie[142:142 + 2], 16)
    temp = "%02x" % (num ^ (ord("e") ^ ord("m")))
    x[142 + 0] = temp[0]
    x[142 + 1] = temp[1]

    num = int(cookie[144:144 + 2], 16)
    temp = "%02x" % (num ^ (ord("r") ^ ord("i")))
    x[144 + 0] = temp[0]
    x[144 + 1] = temp[1]

    num = int(cookie[146:146 + 2], 16)
    temp = "%02x" % (num ^ (0 ^ ord("n")))
    x[146 + 0] = temp[0]
    x[146 + 1] = temp[1]

    num = int(cookie[158:158 + 2], 16)
    temp = "%02x" % (num ^ (6 ^ 5))
    x[158 + 0] = temp[0]
    x[159 + 1] = temp[1]
    """
    
    
    """
    for count in range(0, 14):
        offset = 64 + (count * 2)
        num = int(cookie[offset:offset + 2], 16)
        insert = ord(attack_str[count])
        result = (num ^ (diffX(num, insert) ^ (num)))
        temp = "%02x" % result
        x[offset] = temp[0] 
        x[offset + 1] = temp[1]

    
    """
    """
    num = int(cookie[96 - 32:98 - 32], 16)
    print(num)
    num ^= 1
    print(num)
    temp = "%02x" % num
    x[96 - 32] = temp[0]
    print(temp)
    x[96 - 32 + 1] = temp[1]

    num = int(cookie[106 - 32:108 - 32], 16)
    num ^= 1
    temp = "%02x" % num
    x[106 - 32] = temp[0] 
    x[106 - 32 + 1] = temp[1]

    """
    """
    num = int(cookie[106 - 32:108 - 32], 16)
    num ^= 1
    temp = "%02x" % num
    x[106 - 32] = temp[0] 
    x[106 - 32 + 1] = temp[1]

    num = int(cookie[116 - 32:118 - 32], 16)
    num ^= 1
    temp = "%02x" % num
    x[116 - 32] = temp[0] 
    x[116 - 32 + 1] = temp[1]
    """
    """
    for count in range(0, 16):
        offset = 64 + (count * 2)
        num = int(cookie[offset:offset + 2], 16)
        insert = ord(attack_str[count])
        result = (num ^ (diffX(num, insert) ^ (num)))
        temp = "%02x" % result
        x[offset] = temp[0] 
        x[offset + 1] = temp[1]
    """

    """
    print(cookie[128:160])
    x = list(cookie)
    print(len(x))
    fUpBlock = 0 * 32
    attack_str = "&uid=1&role=adm"
    idx = 0
    cookieTemp = cookie[0 : 192]
    whatChanged = []
    for count in range(0, 15):
        offset = 128 - fUpBlock + (count * 2)
        num = int(cookie[offset:offset + 2], 16)

        if (count == 15):
            insert = ord(attack_str[count]) #- 16
        else:
            insert = ord(attack_str[count])
        whatChanged.append((diffX(num, insert)))
        result = (num ^ (diffX(num, insert) ^ (num)))
        temp = "%02x" % result
        whatChanged.append(result)
        print(attack_str[count], num, temp, offset, offset+2)
        x[offset] = temp[0] 
        x[offset + 1] = temp[1]
        idx += 1

    
    for count in range(0, 16):
        offset = 128 + fUpBlock + (count * 2)
        num2 = int(cookie[offset:offset + 2], 16)
        
        if idx < len(attack_str):
            insert2 = ord(attack_str[idx])
        elif idx < 31:
            insert2 = 0
        else:
            insert2 = 32 - len(attack_str)
        print(insert2, idx, offset, offset + 2)
        num2 = (num2 ^ whatChanged[count])
        temp = "%02x" % num2
        print(offset)
        x[offset] = temp[0]
        x[offset + 1] = temp[1]
        idx += 1
    """

    """
    num = int(cookie[130 - fUpBlock:132 - fUpBlock], 16)
    temp = "%02x" % (diffX(num, ord('u')) ^ (num))
    x[130 - fUpBlock] = temp[0]
    x[131 - fUpBlock] = temp[1]
    print(temp)

    num = int(cookie[130 - fUpBlock:132 - fUpBlock], 16)
    temp = "%02x" % (8 ^ (int(cookie[132- fUpBlock:134 - fUpBlock], 16)))
    x[132 - fUpBlock] = temp[0]
    x[133 - fUpBlock] = temp[1]
    print(temp)

    temp = "%02x" % (27 ^ (int(cookie[134 - fUpBlock:136 - fUpBlock], 16)))
    x[134 - fUpBlock] = temp[0]
    x[135 - fUpBlock] = temp[1]
    print(temp)

    temp = "%02x" % (110 ^ (int(cookie[136 - fUpBlock:138 - fUpBlock], 16)))
    x[136 - fUpBlock] = temp[0]
    x[137 - fUpBlock] = temp[1]
    print(temp)

    temp = "%02x" % (7 ^ (int(cookie[158 - fUpBlock:160 - fUpBlock], 16)))
    x[158 - fUpBlock] = temp[0]
    x[159 - fUpBlock] = temp[1]
    print(temp)
    """   
    
#Task2A()
#Task2B()
Task2C()
#Task2A()
#Task3A()
#Task3B()
