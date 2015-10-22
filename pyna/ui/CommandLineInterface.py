import readline
from pyna.ui.CommandParser import CommandParser
from pyna.ui.PynaDisplay import PynaDisplay

class CommandLineInterface(object):
	'''This is the command line interface. It handles all user input and sends to the processor as necessary'''
	def __init__(self, manager,dispatcher):
		self.parser = CommandParser(manager, dispatcher)
		readline.parse_and_bind('tab: complete')

	# Waits for input from the user, then sends it off to be handled
	def __running__(self):
		'''Our default running loop which governs the UI'''
		while True:
			chat = input('')
			self.parser.parse(chat)
