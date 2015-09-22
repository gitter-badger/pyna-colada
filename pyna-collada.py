import json, socket

class PynaClient(object):
	def __init__(self, server, alias="anonymous"):
		self.authorized_server_list = []
		self.server = server
		self.active_server_list = []
		self.active_aliases = {}

	def display(self, msg):
		displayed_message = "{0}: {1}".format(msg['sender']['name'], msg['message'])
		if msg['type'] == 'whisper':
			# Format this differently
			displayed_message = "{0} <W>: {1}".format(msg['sender']['name'], msg['message'])
		print(displayed_message)

	def activate_server(self, location, alias):
		if location not in self.active_server_list:
			self.active_server_list.append(location)
			print('Activated {0}'.format(location))
		if alias not in self.active_aliases:
			self.active_aliases[alias] = location
			print('Registered {0} at {1}'.format(alias,location))


class PynaServer(object):
	def __init__(self, address='192.168.0.1',port=433):
		self.authorized_server_list = []
		self.client = PynaClient(self);

	def receive(self, message):
		msg = json.load(message)
		if (msg['type'] == 'chat' or msg['type'] == 'whisper'):
			self.client.display(msg)
		if msg['type'] == 'connect':
			self.connect(msg['sender'])
		self.client.activate_server(msg['sender']['location'],msg['sender']['name'])


	def connect(self, sender):
		if sender['location'] not in self.authorized_server_list:
			self.authorized_server_list.append(sender['location'])

var = PynaServer()

# Test Connect
example_connection = open('Examples/connect.json','r')
var.receive(example_connection)

# Test Chat
example_connection = open('Examples/chat.json','r')
var.receive(example_connection)

# Test Whisper
example_connection = open('Examples/whisper.json','r')
var.receive(example_connection)
