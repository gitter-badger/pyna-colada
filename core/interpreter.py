import json
from core.crypto import Crypto

class Interpreter(object):
	def __init__(self, processor, display, manager):
		self.display = display
		self.manager = manager
		self.processor = processor
	# Handles receipt of the actual json we take in
	def interpret_message(self,enc_msg):
		'''
		Decrypt and identify message
		'''
		# add this server to our list since we know it's real
		jsmsg = self.crypto.decrypt(enc_msg)
		msg = json.loads(jsmsg.strip())
		#self.display.debug('{0} received\n{1}'.format(msg['type'],msg))
		self.check_node_status(msg['sender'])
		# Determine what needs to be done according to the message type
		self.handleMessageType(msg)

	def handleMessageType(self,msg):
		'''
		Figure out what to do with a received message
		'''
		sender = msg['sender']
		if msg['type'] == 'ping':
			self.processor.send("pingReply",sender['location'])
			return
		if msg['type'] == 'disconnection':
			self.manager.deactivate_node(sender)
			self.display.disconnected(sender['alias'],sender['location'])
			return
		if 'nodeList' in msg['type']:
			self.interpret_node_list(msg,sender)
			return
		if msg['type'] == 'whisper':
			self.manager.most_recent_whisperer = sender['alias']
		self.display.display(msg)

	def interpret_node_list(self,msg,sender):
		if msg['type'] == 'nodelisthash':
			if not self.manager.hash_is_identical(msg['message']):
				self.processor.full_node_list(sender['location'])
			else: self.display.debug('Hashes are identical with {0}'.format(sender['alias']))
			return
		if msg['type'] == 'nodelistfull':
			unique_to_sender = self.manager.diff_node_list(msg['message'])
			self.processor.node_list_diff(unique_to_sender,sender['location'])
			self.processor.broadcast('ping',targets=self.manager.authorized_nodes)
			return
		if msg['type'] == 'nodelistdiff':
			diffed_nodes = self.manager.add_nodes(msg['message'])
			self.processor.broadcast('ping',targets=diffed_nodes)
			return

	# For new connections
	def check_node_status(self, sender):
		# tell the client to try to activate the server
		location = sender['location']
		alias = sender['alias']
		# If this is not active... activate it! Then NodeListHash it
		if self.manager.activate_node(sender):
			self.processor.node_list_hash(sender['location'])
			self.display.log('Registered {0} at {1}'.format(alias,location))
