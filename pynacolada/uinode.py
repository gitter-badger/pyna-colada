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
		# Base Components
		self.display = Display()
		self.crypto = Crypto(self.display)
		self.sender = Sender(self.crypto)

		self.relay = Relay(self.sender,self.display,self.manager)
		self.processor = Processor(self.relay,self.display, self.manager)
		self.interpreter = Interpreter(self.processor,self.display,self.manager)
		self.cli = CommandLineInterface(self.processor,self.display)

		# Crypto
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
