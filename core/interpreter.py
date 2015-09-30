import json

class Interpreter(object):
	def __init__(self, processor, display, manager):
		self.display = display
		self.manager = manager
		self.processor = processor

	# Handles receipt of the actual json we take in
	def interpret_message(self,msg):
		sender_location = msg['sender']['address']
		# add this server to our list since we know it's real
		self.check_node_status(msg['sender'])
		# Determine what needs to be done according to the message type
		if msg['type'] == 'ping':
			self.processor.send("pingReply",sender_location)
			return
		if msg['type'] == 'disconnection':
			self.manager.deactivate_node(msg['sender'])
			self.display.disconnected(msg['sender']['alias'],sender_location)
			return
		if msg['type'] == 'connection':
			self.processor.node_list_hash(sender_location)
			return
		if msg['type'] == 'nodeListHash':
			if not self.manager.hash_is_identical(msg['message']):
				self.processor.full_node_list(sender_location)
			return
		if msg['type'] == 'nodeListFull':
			diffed_nodes = self.manager.diff_node_list(msg['message'])
			self.processor.node_list_diff(diffed_nodes,sender_location)
			return
		if msg['type'] == 'nodeListDiff':
			diffed_nodes = self.manager.add_nodes(msg['message'])
			return
		if msg['type'] == 'whisper':
			self.manager.most_recent_whisperer = msg['sender']['alias']
		self.log_message(msg)
		self.display.display(msg)

	def log_message(self,msg):
		pass
		#if self.manager.logger != "":
		#	self.processor.whisper('Received {0} from {1}@{2}'.format(msg['type'],msg['sender']['name'],msg['sender']['location']),self.manager.logger)

	# For new connections
	def check_node_status(self, sender):
		# tell the client to try to activate the server
		location = sender['address']
		alias = sender['alias']

		# Check to see if it is in our authorized_server_list, add it if not
		#if self.manager.authorize(sender):
		self.manager.authorize(sender)
	#		self.display.log("Authorized {0} (uid: {1}) at {2}".format(sender['name'],sender['uid'],sender['location']))

		# Check to see if active; if not, send it a serverlisthash
	#	if self.manager.activate_server(sender['location']):
	#		self.relay.send_type_to_location('serverlisthash',location)

		if self.manager.activate_node(sender):
			self.display.log('Registered {0} at {1}'.format(alias,location))
