# Sean Sheen & Zach Mintzer
# CSC323 Lab3, Task 4
import requests
import base64
import datetime
import urllib2

def constantTimeCompare(message, message_new):
    value = 0
    for x, y in zip(message, message_new):
        value |= ord(x) ^ ord(y)
    return value == 0

macLength = 20

testTag = chr(98) + chr(97) * 19

solutionString = ""
urlString = ""
user = "foo"
maxTime = datetime.timedelta(microseconds=0)
previousTime = datetime.timedelta(microseconds=0)
maxChar = 0
done = 0
j = 1
tries = 0
#finding the delay in compare

for i in range(0, 256):
    timeAvg = datetime.timedelta(microseconds=0)
    testString = chr(i) + testTag[1:]
    testString = base64.b16encode(testString)
    testString = testString.lower()
    testvalues = {'q' : user, 'mac': testString}

    for k in range(0, 5):
        r = requests.get("http://127.0.0.1:8080", params = testvalues)
        timeAvg+=r.elapsed
    if timeAvg > maxTime:
        maxTime = timeAvg
        maxChar = i

print("Max Time: " + str(maxTime/5) + " Char: " + str(maxChar))
maxTime = maxTime/5
#once max char is found, find the average time of fail for comparison
timeAvg = datetime.timedelta(microseconds=0)
for i in range(0, 5):
    testString = chr(maxChar - 1) + testTag[1:]
    testString = base64.b16encode(testString)
    testString = testString.lower()
    print(testString, type(testString))
    testvalues = {'q' : user, 'mac': testString}
    r = requests.get("http://127.0.0.1:8080", params = testvalues)
    timeAvg+=r.elapsed

timeAvg = timeAvg/5
newTime = maxTime - timeAvg
print("1 compare: " + str(maxTime))
print("Fail compare: " + str(timeAvg))
print("Difference: " + str(newTime))
print(str(newTime.microseconds))
delayTime = newTime.microseconds/2

while (done == 0):
   maxTime = datetime.timedelta(microseconds=0)
   d = datetime.timedelta(microseconds=0)
   maxChar = 0
   for i in range(0, 256):
      testString = solutionString + chr(i) + testTag[j:]
      testString = base64.b16encode(testString)
      testString = testString.lower()
      print("tesr:")
      print("Hello: ", testString, type(testString))
      testvalues = {'q' : 'foo', 'mac': testString}

      for k in range(0, 1):
         r = requests.get("http://127.0.0.1:8080", params = testvalues)
         d += r.elapsed

      if d > maxTime:
         maxTime = d
         maxChar = i

      d = datetime.timedelta(microseconds=0)
   tries+=1
   if (maxTime - previousTime > datetime.timedelta(microseconds=0) and maxTime - previousTime > datetime.timedelta(microseconds=5000)):
      print("Max char: " + str(maxChar) + " MaxTime: " + str(maxTime) + " PrevTime: " + str(previousTime))
      previousTime = maxTime
      solutionString = solutionString + chr(maxChar)
      j+=1
      tries=0
   elif tries == 3:
      tries = 0
      j-=1
      print(len(solutionString))
      solutionString = solutionString[:-1]
      print(len(solutionString))
      previousTime = datetime.timedelta(microseconds=0)


   print("Max Time: " + str(maxTime) + " PrevTime: " + str(previousTime))
   print("Current solution length: " + str(len(solutionString)))
   if (j == 21):
      done = 1

print(solutionString)
solutionString = base64.b16encode(solutionString)
print(solutionString)
print(user)
t = solutionString
for x in range(0, 256):
  temp = t + ("%02x" % x)
  #print(temp)
  values = {'q':"foo", 'mac':temp}
  r = requests.get("http://127.0.0.1:8080", params = values)
  if not 'Invalid' in r.text:
    print(r.text, x)