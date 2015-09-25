import threading, time, json
from listener import Listener
from sender import Sender
from display import Display
from packager import Packager
from interpreter import Interpreter
from inputhandler import InputHandler
from cli import CommandLineInterface
from configuration import Configuration

class Node(object):
	def __init__(self,alias,address,port):
		self.address = address
		self.port = port
		self.configuration = Configuration(alias,address,port)
		# Build the client
		self.start(alias)

	def start(self, alias):
		self.packager = self.configuration.create_packager()
		self.display = Display()
		self.sender = Sender(self.display)
		self.inputhandler = InputHandler(self.sender,self.display,self.packager,self.configuration)
		self.interpreter = Interpreter(self.inputhandler,self.display,self.packager,self.configuration)
		self.cli = CommandLineInterface(self.inputhandler)
		self.display.pyna_colada(self.configuration.version)
		# start the server up
		self.listener = Listener(alias,self.display,self.interpreter,self.address,int(self.port))
		self.interpreter.display = self.display

		listener_thread = threading.Thread(target=self.listener.__running__)
		listener_thread.daemon = True
		listener_thread.start()

		# Await initialization before starting client thread
		time.sleep(1)
		sender_thread = threading.Thread(target=self.cli.__running__)
		sender_thread.start()
