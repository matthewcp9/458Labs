import urllib 
import urllib2

def getCT():
	url = 'http://localhost:8080/eavesdrop'
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	return x.split('<p><font color="red"> ')[1].split(' </font>')[0]

def queryWebsite():
	cipherTxt = getCT()
	
