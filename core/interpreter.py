import json

class Interpreter(object):
	def __init__(self, inputhandler, display, servermanager):
		self.display = display
		self.manager = servermanager
		self.inputhandler = inputhandler

	# Handles receipt of the actual json we take in
	def interpret_message(self,msg):
		sender_location = msg['sender']['location']
		# add this server to our list since we know it's real
		self.connect(msg['sender'])
		# Determine what needs to be done according to the message type
		if msg['type'] == 'ping':
			self.inputhandler.send_type_to_location('pingreply',sender_location)
			return
		if msg['type'] == 'disconnection':
			self.inputhandler.deactivate_server(sender_location)
			self.display.disconnected(msg['sender']['name'],sender_location)
			return
		if msg['type'] == 'connection':
			self.inputhandler.send_type_to_location('serverlisthash',sender_location)
			return
		if msg['type'] == 'whisper':
			self.manager.most_recent_whisperer = msg['sender']['name']
		self.log_message(msg)
		self.display.display(msg)

	def ping_all(self):
		self.inputhandler.ping_all()

	def log_message(self,msg):
		if self.manager.logger != "":
			self.inputhandler.send_text_message('Received {0} from {1}@{2}'.format(msg['type'],msg['sender']['name'],msg['sender']['location']),self.manager.logger)

	# For new connections
	def connect(self, sender):
		# tell the client to try to activate the server
		self.inputhandler.activate_server(sender['location'],sender['name'])
		# Check to see if it is in our authorized_server_list, add it if not
		if sender['location'] not in self.manager.authorized_server_list:
			self.manager.authorized_server_list.append(sender['location'])
			# Update our servers.json with the new server info
			data = json.load(open('config/servers.json','r'))
			data.update({"servers":self.manager.authorized_server_list})
			with open('config/servers.json','w') as auth:
				json.dump(data, auth)
