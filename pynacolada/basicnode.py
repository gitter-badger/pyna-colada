import threading, time, json
from pynacolada.base.crypto import Crypto
from pynacolada.base.display import Display
from pynacolada.base.listener import Listener
from pynacolada.base.sender import Sender
from pynacolada.core.interpreter import Interpreter
from pynacolada.core.manager import Manager
from pynacolada.core.packager import Packager
from pynacolada.core.processor import Processor
from pynacolada.core.relay import Relay
from pynacolada.ui.cli import CommandLineInterface

class BasicNode(object):
	'''Main PyNa Colada class. This initializes and handles threads for Pyna Colada'''

	def __init__(self,alias,location,port):
		self.location = location
		self.port = port
		self.manager = Manager(alias,location,port)

	def start(self):
		'''Start up this node'''
		self.initialize_components()
		self.start_up_listener()

		# Provide information to user and other clients (the latter via ping)
		self.display.pyna_colada(self.manager.version)
		self.display.log('Node running on {0}:{1}\n'.format(self.location,self.port))
		self.processor.broadcast('ping',targets=self.manager.node_list.authorized_nodes)

		# Await initialization before starting client thread
		time.sleep(1)
		sender_thread = threading.Thread(target=self.cli.__running__)
		sender_thread.start()

	def initialize_components(self):
		'''
		Build up all components in the node
		'''
		self.display = Display()
		self.sender = Sender()
		self.relay = Relay(self.sender,self.display,self.manager)
		self.processor = Processor(self.relay,self.display, self.manager)
		self.interpreter = Interpreter(self.processor,self.display,self.manager)
		self.cli = CommandLineInterface(self.processor,self.display)

		# Crypto
		crypto = Crypto(self.display)
		self.relay.crypto = crypto
		self.interpreter.crypto = crypto
		self.manager.crypto = crypto

	def start_up_listener(self):
		'''Set up the listener thread separately'''
		self.listener = Listener(int(self.port),self.interpreter)
		# thread
		listener_thread = threading.Thread(target=self.listener.__launch__)
		listener_thread.daemon = True
		listener_thread.start()
