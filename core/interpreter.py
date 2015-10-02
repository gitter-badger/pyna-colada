import json

class Interpreter(object):
	def __init__(self, processor, display, manager):
		self.display = display
		self.manager = manager
		self.processor = processor

	# Handles receipt of the actual json we take in
	def interpret_message(self,msg):
		'''Figure out what to do with a received message'''
		# add this server to our list since we know it's real
		sender = msg['sender']
		self.check_node_status(sender)
		# Determine what needs to be done according to the message type
		if msg['type'] == 'ping':
			self.processor.send("pingReply",sender['address'])
			return
		if msg['type'] == 'disconnection':
			self.manager.deactivate_node(sender)
			self.display.disconnected(sender['alias'],sender['address'])
			return
		if msg['type'] == 'connection':
			self.processor.node_list_hash(sender['address'])
			return
		if 'nodeList' in msg['type']:
			self.interpret_node_list(msg,sender)
			return
		if msg['type'] == 'whisper':
			self.manager.most_recent_whisperer = sender['alias']
		self.display.display(msg)

	def interpret_node_list(self,msg,sender):
		if msg['type'] == 'nodeListHash':
			if not self.manager.hash_is_identical(msg['message']):
				self.processor.full_node_list(sender['address'])
			return
		if msg['type'] == 'nodeListFull':
			unique_to_sender = self.manager.diff_node_list(msg['message'])
			self.processor.node_list_diff(unique_to_sender,sender['address'])
			self.processor.broadcast('ping',targets=self.manager.authorized_nodes)
			return
		if msg['type'] == 'nodeListDiff':
			diffed_nodes = self.manager.add_nodes(msg['message'])
			self.processor.broadcast('ping',targets=diffed_nodes)
			return

	# For new connections
	def check_node_status(self, sender):
		# tell the client to try to activate the server
		location = sender['address']
		alias = sender['alias']
		self.manager.authorize(sender)
		if self.manager.activate_node(sender):
			self.display.log('Registered {0} at {1}'.format(alias,location))
