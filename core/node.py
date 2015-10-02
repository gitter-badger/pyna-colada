import threading, time, json
from core.listener import Listener
from core.sender import Sender
from core.display import Display
from core.packager import Packager
from core.interpreter import Interpreter
from core.relay import Relay
from core.cli import CommandLineInterface
from core.manager import Manager
from core.processor import Processor

class Node(object):
	'''Overseer. This initializes and handles threads for Pyna Colada'''

	def __init__(self,alias,address,port):
		self.address = address
		self.port = port
		self.manager = Manager(alias,address,port)

	def start(self):
		self.initialize_components()

		# start up Listener
		self.start_up_listener()

		# information
		self.display.pyna_colada(self.manager.version)
		self.display.log('Node running on {0}:{1}\n'.format(self.address,self.port))
		self.processor.broadcast('connection',targets=self.manager.authorized_nodes)

		# Await initialization before starting client thread
		time.sleep(1)
		sender_thread = threading.Thread(target=self.cli.__running__)
		sender_thread.start()

	def initialize_components(self):
		self.display = Display()
		self.sender = Sender(self.display)
		self.relay = Relay(self.sender,self.display,self.manager)
		self.processor = Processor(self.relay,self.display, self.manager)
		self.interpreter = Interpreter(self.processor,self.display,self.manager)
		self.interpreter.display = self.display
		self.cli = CommandLineInterface(self.processor,self.display)

	def start_up_listener(self):
		self.listener = Listener(self.interpreter,self.address,int(self.port))
		self.listener.display = self.display
		# thread
		listener_thread = threading.Thread(target=self.listener.__running__)
		listener_thread.daemon = True
		listener_thread.start()
