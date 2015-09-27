import threading, time, json
from core.listener import Listener
from core.sender import Sender
from core.display import Display
from core.packager import Packager
from core.interpreter import Interpreter
from core.inputhandler import InputHandler
from core.cli import CommandLineInterface
from core.servermanager import ServerManager

class Node(object):
	def __init__(self,alias,address,port):
		self.address = address
		self.port = port
		self.servermanager = ServerManager(alias,address,port)
		# Build the client
		self.start()

	def start(self):
		self.initialize_components()

		# start up Listener
		self.start_up_listener()

		# information
		self.display.pyna_colada(self.servermanager.version)
		self.display.log('Node running on {0}:{1}\n'.format(self.address,self.port))
		self.inputhandler.ping_all()

		# Await initialization before starting client thread
		time.sleep(1)
		sender_thread = threading.Thread(target=self.cli.__running__)
		sender_thread.start()

	def initialize_components(self):
		self.display = Display()
		self.sender = Sender(self.display)
		self.inputhandler = InputHandler(self.sender,self.display,self.servermanager)
		self.interpreter = Interpreter(self.inputhandler,self.display,self.servermanager)
		self.interpreter.display = self.display
		self.cli = CommandLineInterface(self.inputhandler)

	def start_up_listener(self):
		self.listener = Listener(self.interpreter,self.address,int(self.port))
		self.listener.display = self.display
		# thread
		listener_thread = threading.Thread(target=self.listener.__running__)
		listener_thread.daemon = True
		listener_thread.start()
