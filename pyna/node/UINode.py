from pyna.core.Crypto import Crypto
from pyna.core.Dispatcher import Dispatcher
from pyna.core.Listener import Listener
from pyna.core.Manager import Manager
from pyna.core.Sender import Sender
from pyna.server.MessageParser import MessageParser
from pyna.ui.CommandLineInterface import CommandLineInterface
from pyna.ui.PynaDisplay import PynaDisplay

import json, threading, time

class UINode(object):
	'''Main PyNa Colada class. This initializes and handles threads for Pyna Colada'''

	def __init__(self,alias,location,port):
		self.location = location
		self.port = port
		self.alias = alias
		self.manager = Manager(alias,location,port)
		self.uid = self.manager.uid #TODO: Remove the need for manager's UID?


	def initialize(self):
		# Base Components
		self.crypto = Crypto(self.manager.uid)
		self.listener = Listener(self.crypto)
		self.sender = Sender(self.crypto)
		self.dispatcher = Dispatcher(self.manager, self.sender)

		# Server and UI
		self.ui = CommandLineInterface(self.manager, self.dispatcher)
		self.server = MessageParser(self.manager, self.dispatcher)

		# Connect the Parser
		self.listener.attachParser(self.server)


	def start(self):
		'''Start up this node'''
		self.initialize()
		self.export()
		self.start_up_listener()

		# Provide information to user and other clients (the latter via ping)
		PynaDisplay.splash(self.manager.version)
		PynaDisplay.log('Node running on {0}:{1}\n'.format(self.location,self.port))
		self.dispatcher.broadcast('ping',targets=self.manager.node_list.authorized_nodes)

		# Await initialization before starting client thread
		time.sleep(1)
		sender_thread = threading.Thread(target=self.ui.__running__)
		sender_thread.start()


	def start_up_listener(self):
		'''Set up the listener thread separately'''
		listener_thread = threading.Thread(target=self.listener.__launch__, args=(int(self.port),))
		listener_thread.daemon = True
		listener_thread.start()


	def export(self):
		# Build Data Object
		data = {"uid": self.uid, "alias": self.alias, "location": ':'.join([self.location,self.port])}
		data["publicKey"] = self.crypto.getPublic().decode('utf-8')

		with open('{0}.json'.format(self.alias),'w') as auth:
			json.dump(data, auth)
