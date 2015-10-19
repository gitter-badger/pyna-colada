import json
from core.crypto import Crypto

class Interpreter(object):
	def __init__(self, processor, display, manager):
		self.display = display
		self.manager = manager
		self.processor = processor
	# Handles receipt of the actual json we take in
	def interpretMessage(self,enc_msg):
		'''
		Decrypt and identify message
		'''
		# add this server to our list since we know it's real
		msg = self.crypto.decrypt(enc_msg)
		#self.display.debug('{0} received\n{1}'.format(msg['type'],msg))
		need_to_nlh = self.check_node_status(msg['sender'])
		self.handleMessageType(msg)
		if need_to_nlh:
			self.processor.node_list_hash(msg['sender'])

	def handleMessageType(self,msg):
		'''
		Figure out what to do with a received message
		'''
		sender = msg['sender']
		if msg['type'] == 'ping':
			# May not always work (in the handshakes)
			self.processor.send("pingReply",sender['location'])
			return
		if msg['type'] == 'disconnection':
			self.manager.deactivate_node(sender)
			self.display.disconnected(sender['alias'],sender['location'])
			return
		if 'nodelist' in msg['type']:
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
		if msg['type'] == 'nodelistdiff':
			diffed_nodes = self.manager.node_list.addList(msg['message'])
			self.processor.broadcast('ping',targets=diffed_nodes)
			return
		if msg['type'] == 'nodelist':
			unique_to_sender = self.manager.node_list.diff(msg['message'])
			if len(unique_to_sender) > 0:
				self.processor.node_list_diff(unique_to_sender,sender['location'])
			self.processor.broadcast('ping',targets=self.manager.node_list.authorized_nodes)
			return

	# For new connections
	def check_node_status(self, sender):
		# tell the client to try to activate the server
		# If this is not active... activate it! Then NodeListHash it
		if self.manager.activate_node(sender):
			self.display.log('Registered {0} at {1}'.format(sender['alias'],sender['location']))
			return True
		return False
