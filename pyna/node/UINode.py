from pyna.server.MessageParser import MessageParser
from pyna.ui.CommandLineInterface import CommandLineInterface
from pyna.ui.PynaDisplay import PynaDisplay

from pyna.node.BaseNode import BaseNode
import json, threading, time

class UINode(BaseNode):
	'''Pyna Colada node with User Interface'''

	def initialize(self):
		'''Initialize, then add the server and UI'''
		super().initialize()

		# Server and UI
		self.ui = CommandLineInterface(self.manager, self.dispatcher)
		self.server = MessageParser(self.manager, self.dispatcher)

		# Connect the Parser
		self.listener.attachParser(self.server)


	def __running__(self):
		'''Start up client thread, '''

		# Provide information to user about its location and the client
		PynaDisplay.splash(self.manager.version)
		PynaDisplay.log('Node running on {0}:{1}\n'.format(self.location,self.port))

		# Await initialization before starting client thread
		time.sleep(1)
		sender_thread = threading.Thread(target=self.ui.__running__)
		sender_thread.start()
