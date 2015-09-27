from core.inputhandler import InputHandler

class CommandLineInterface(object):
	def __init__(self,inputhandler):
		self.inputhandler = inputhandler

	# Waits for input from the user, then sends it off to be handled
	def __running__(self):
		while True:
			chat = input('')
			self.inputhandler.process(chat)
