import requests

t = "07FF79F7DA55403868ECAFB8EF48170D96761E".lower()

for x in range(0, 256):
	temp = t + ("%02x" % x)
	#print(temp)
	values = {'q':"foo", 'mac':temp}
	r = requests.get("http://127.0.0.1:8080", params = values)
	if not 'Invalid' in r.text:
		print(r.text, x)