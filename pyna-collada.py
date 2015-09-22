import json, socket, requests, struct, codecs

class PynaClient(object):
	def __init__(self, location, alias="anonymous"):
		self.authorized_server_list = []
		self.alias = alias
		self.location = location
		self.active_server_list = []
		self.active_aliases = {}

	# show a message on the client
	def display(self, msg):
		displayed_message = "{0}: {1}".format(msg['sender']['name'], msg['message'])
		if msg['type'] == 'whisper':
			# Format this differently
			displayed_message = "{0} <W>: {1}".format(msg['sender']['name'], msg['message'])
		print(displayed_message)

	# Try to activate the server, or at least the alias
	def activate_server(self, location, alias):
		if location not in self.active_server_list:
			self.active_server_list.append(location)
			print('Activated {0}'.format(location))
		if alias not in self.active_aliases:
			self.active_aliases[alias] = location
			print('Registered {0} at {1}'.format(alias,location))

	# Send JSON to all active servers
	def send_chat(self,json):
		for active_server in self.active_server_list:
			request_receipt = requests.post('http://{0}'.format(active_server), json=json)

	# Send JSON to a whisper target
	def send_whisper(self,target_alias,json):
		if target_alias in activate_aliases:
			request_receipt = requests.post('http://{0}'.format(active_server), json=json)

	# Package up our data. Most of this will be in a json file, but we're not quite there yet
	def package(self,message_type,message):
		data = {}
		data['type'] = message_type
		data['client'] = 'Pyña colada'
		data['client_version'] = 'v0.0.1'
		data['sender'] = {'name': self.alias, 'location': self.server.address}
		data['message'] = message
		return data


class PynaServer(object):
	def __init__(self, client, address='localhost',port=2008):
		self.authorized_server_list = []
		self.client = client
		self.address = address
		self.listen(port)

	# This is the big part where we are waiting for messages
	def listen(self,port):
		try:
			# Try to bind the socket
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket.bind((self.address, port))
			print('Socket bound appropriately')
		except socket.error as msg:
			# No dice. Kill the process.
			print('Unable to bind socket: {0}'.format(msg))
			return
		self.socket.listen(1)
		while 1:
			# Now we wait
			connection, address = self.socket.accept()
			response = connection.recv(1024)
			(headers, js) = response.decode('utf-8').split("\r\n\r\n")
			self.receive(js)

	# Handles receipt of the actual json we take in
	def receive(self, message):
		msg = json.loads(message)
		if (msg['type'] == 'chat' or msg['type'] == 'whisper'):
			self.client.display(msg)
		if msg['type'] == 'connect':
			self.connect(msg['sender'])
		# Nonetheless, try to activate the server on the client
		self.client.activate_server(msg['sender']['location'],msg['sender']['name'])

	# For new connections
	def connect(self, sender):
		if sender['location'] not in self.authorized_server_list:
			self.authorized_server_list.append(sender['location'])

client = PynaClient('localhost')
server = PynaServer(client)
