import sys
from pyna.base.Interpreter import Interpreter
from pyna.core.Dispatcher import Dispatcher
from pyna.core.Manager import Manager
from pyna.ui.PynaDisplay import PynaDisplay

class MessageInterpreter(Interpreter):
	'''Interprets a received message and sends to Dispatcher if necessary'''
	def __init__(self, manager, dispatcher):
		self.manager = manager
		self.dispatcher = dispatcher

	def received_ping(self,msg):
		self.dispatcher.send(type="pingreply", target=msg['sender'])

	def received_disconnection(self,msg):
		self.manager.deactivate_node(msg['sender'])
		PynaDisplay.disconnected(msg['sender'])

	def received_nodelist(self,msg):
		unique_to_sender = self.manager.node_list.diff(msg['message'])
		if len(unique_to_sender) > 0:
			self.dispatcher.send('nodelistdiff', target=sender, content=unique_to_sender)

		# Assemble message
		targets=self.manager.node_list.authorized_nodes
		content=self.manager.get_node_hash()
		self.dispatcher.broadcast('ping', targets=targets, content=content)

	def received_nodelistdiff(self,msg):
		targets  = self.manager.node_list.addList(msg['message'])
		self.dispatcher.broadcast('ping', targets=targetrs)

	def received_nodelisthash(self,msg):
		if self.manager.hash_is_identical(msg['message']):
			return
		node_list = self.manager.get_node_list()
		self.dispatcher.send('nodelist', content=node_list, target=msg['sender'])

	def received_whisper(self, msg):
		self.manager.most_recent_whisperer = msg['sender']
		self.received_chat(msg)

	def received_chat(self,msg):
		PynaDisplay.display(msg)

	def received_pingreply(self,msg):
		pass
