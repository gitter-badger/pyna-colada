import json, requests, struct

json = json.load(open('Examples/connect.json','r'))

try:
	requests.post('http://localhost:2008', json=json,headers={'Connection':'close'})
except:
	print('Connection closed')
