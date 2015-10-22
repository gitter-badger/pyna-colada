from pyna.server.MessageParser import MessageParser
from pyna.ui.CommandLineInterface import CommandLineInterface
from pyna.ui.PynaDisplay import PynaDisplay

from pyna.node.BaseNode import BaseNode
import json, threading, time, sys

class AutonomousNode(BaseNode):
	'''Main PyNa Colada class. This initializes and handles threads for Pyna Colada'''

	def initialize(self):
		'''Initialize, then add the server'''

		# Base Components
		super().initialize()

		# Connect the server
		self.server = MessageParser(self.manager, self.dispatcher)
		self.listener.attachParser(self.server)


	def __running__(self):
		'''Run until receiving 'q'''
		killmsg = ''
		while killmsg != 'q':
			killmsg = input('')

		sys.exit(0)
