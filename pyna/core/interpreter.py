import json
from pyna.base.crypto import Crypto
from pyna.base.display import Display

class Interpreter(object):
	def __init__(self, processor, manager):
		self.manager = manager
		self.processor = processor

	# Handles receipt of the actual json we take in
	def interpret(self,msg):
		'''
		Figure out what to do with this message
		'''
		#Display.debug('{0} received\n{1}'.format(msg['type'],msg))

		needs_activation = self.senderNeedsActivation(msg['type'],msg['sender'])
		self.handleMessageType(msg)
		if needs_activation:
			self.processor.node_list_hash(msg['sender'])

	def handleMessageType(self,msg):
		'''
		Figure out what to do with a received message
		'''
		sender = msg['sender']

		if msg['type'] == 'ping':
			# May not always work (in the handshakes)
			self.processor.send("pingreply",sender['location'])
			return
		if msg['type'] == 'disconnection':
			self.manager.deactivate_node(sender)
			Display.disconnected(sender['alias'],sender['location'])
			return
		if 'nodelist' in msg['type']:
			self.interpret_node_list(msg,sender)
			return
		if msg['type'] == 'whisper':
			self.manager.most_recent_whisperer = sender['alias']

		Display.display(msg)

	def interpret_node_list(self,msg,sender):
		if msg['type'] == 'nodelisthash':
			if not self.manager.hash_is_identical(msg['message']):
				self.processor.full_node_list(sender)
			return

		if msg['type'] == 'nodelistdiff':
			diffed_nodes = self.manager.node_list.addList(msg['message'])
			self.processor.broadcast('ping',content=self.manager.get_node_hash(),targets=diffed_nodes)
			return

		if msg['type'] == 'nodelist':
			unique_to_sender = self.manager.node_list.diff(msg['message'])
			if len(unique_to_sender) > 0:
				self.processor.send('nodelistdiff',sender,content=unique_to_sender)
			self.processor.broadcast('ping',content=self.manager.get_node_hash(),targets=self.manager.node_list.authorized_nodes)
			return

	# For new connections
	def senderNeedsActivation(self, message, sender):
		if self.manager.isActive(sender):
			return False

		if self.manager.isAuthorized(sender):
			self.manager.activate_node(sender)
			Display.log('Registered {0} at {1}'.format(sender['alias'],sender['location']))
			return True

		return self.isAcceptableAnonymousMessage(message,sender)

	def isAcceptableAnonymousMessage(self,message,sender):
		'''Verifies that the message is authorizable'''
		if  message != 'nodelist':
			Display.warn('Untrusted message received from {0}'.format(sender))
			return False

		return True
