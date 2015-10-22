import json
from pyna.base.Parser import Parser
from pyna.core.Crypto import Crypto
from pyna.server.MessageInterpreter import MessageInterpreter
from pyna.ui.PynaDisplay import PynaDisplay

class MessageParser(Parser):
	def __init__(self, manager,dispatcher):
		self.manager = manager
		self.dispatcher = dispatcher
		self.interpreter = MessageInterpreter(manager,dispatcher)


	def handleMessage(self,msg):
		'''
		Figure out what to do with this message
		'''
		needs_activation = self.senderNeedsActivation(msg['type'],msg['sender'])
		self.parse(msg)

		if needs_activation:
			content=self.manager.get_node_hash()
			self.dispatcher.send('nodelisthash', target=msg['sender'], content=content)


	def parse(self,msg):
		'''	Figures out what message type was given, then passes it to MessageProcessor	'''
		method_type = 'received_{0}'.format(msg['type'])
		try:
			method = getattr(self.interpreter,method_type)
			method(msg)
		except:
			self.interpreter.received_chat(msg)


	def senderNeedsActivation(self, message, sender):
		'''Checks to see if the sender is active or even authorized'''
		if self.manager.isActive(sender):
			return False

		if self.manager.isAuthorized(sender):
			self.manager.activate_node(sender)
			PynaDisplay.log('Registered {0} at {1}'.format(sender['alias'],sender['location']))
			return True

		return self.isAcceptableAnonymousMessage(message,sender)


	def isAcceptableAnonymousMessage(self,message,sender):
		'''Verifies that the message is authorizable'''
		if  message != 'nodelist':
			PynaDisplay.warn('Untrusted message received from {0}'.format(sender))
			return False

		return True
