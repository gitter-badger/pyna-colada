import threading, time, json
from pyna.base.crypto import Crypto
from pyna.base.display import Display
from pyna.base.listener import Listener
from pyna.base.sender import Sender
from pyna.core.interpreter import Interpreter
from pyna.core.manager import Manager
from pyna.core.packager import Packager
from pyna.core.processor import Processor
from pyna.core.relay import Relay
from pyna.ui.cli import CommandLineInterface

class UINode(object):
	'''Main PyNa Colada class. This initializes and handles threads for Pyna Colada'''

	def __init__(self,alias,location,port):
		self.location = location
		self.port = port
		self.alias = alias
		self.manager = Manager(alias,location,port)
		self.uid = self.manager.uid #TODO: Remove the need for manager's UID?

	def start(self):
		'''Start up this node'''
		self.initialize_components()
		self.start_up_listener()

		# Provide information to user and other clients (the latter via ping)
		Display.log('Node running on {0}:{1}\n'.format(self.location,self.port))
		self.processor.broadcast('ping',targets=self.manager.node_list.authorized_nodes)

		# Await initialization before starting client thread
		time.sleep(1)
		sender_thread = threading.Thread(target=self.cli.__running__)
		sender_thread.start()

	def initialize_components(self):
		'''
		Build up all components in the node
		'''
		# Base Components
		self.crypto = Crypto()
		self.sender = Sender(self.crypto)

		# Core Pyna Colada Components
		self.relay = Relay(self.sender,self.manager)
		self.processor = Processor(self.relay, self.manager)
		self.interpreter = Interpreter(self.processor,self.manager)

		# UI
		self.cli = CommandLineInterface(self.processor)

		# Listener (since it requires an interpreter)
		self.listener = Listener(self.crypto,self.interpreter)
		self.export()

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
