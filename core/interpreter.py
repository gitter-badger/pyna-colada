import json

class Interpreter(object):
	def __init__(self, processor, display, servermanager):
		self.display = display
		self.manager = servermanager
		self.processor = processor

	# Handles receipt of the actual json we take in
	def interpret_message(self,msg):
		sender_location = msg['sender']['location']
		# add this server to our list since we know it's real
		self.check_node_status(msg['sender'])
		# Determine what needs to be done according to the message type
		if msg['type'] == 'ping':
			self.processor.pingreply(sender_location)
			return
		if msg['type'] == 'disconnection':
			self.manager.dactivate_node(sender)
			self.display.disconnected(msg['sender']['name'],sender_location)
			return
		if msg['type'] == 'connection':
			self.processor.serverlisthash(sender_location)
			return
		if msg['type'] == 'whisper':
			self.manager.most_recent_whisperer = msg['sender']['name']
		self.log_message(msg)
		self.display.display(msg)

	def ping_all(self):
		self.inputhandler.ping_all()

	def log_message(self,msg):
		pass
		#if self.manager.logger != "":
		#	self.processor.whisper('Received {0} from {1}@{2}'.format(msg['type'],msg['sender']['name'],msg['sender']['location']),self.manager.logger)

	# For new connections
	def check_node_status(self, sender):
		# tell the client to try to activate the server
		location = sender['location']
		alias = sender['name']

		# Check to see if it is in our authorized_server_list, add it if not
		#if self.manager.authorize(sender):
		self.manager.authorize(sender)
	#		self.display.log("Authorized {0} (uid: {1}) at {2}".format(sender['name'],sender['uid'],sender['location']))

		# Check to see if active; if not, send it a serverlisthash
	#	if self.manager.activate_server(sender['location']):
	#		self.relay.send_type_to_location('serverlisthash',location)

		if self.manager.activate_node(sender):
			self.display.log('Registered {0} at {1}'.format(alias,location))
