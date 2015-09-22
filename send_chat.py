import json, requests, struct

json = json.load(open('Examples/whisper.json','r'))

requests.post('http://localhost:2008', json=json)
