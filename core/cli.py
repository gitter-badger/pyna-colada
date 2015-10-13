#import readline
from core.processor import Processor

class CommandLineInterface(object):
	'''This is the command line interface. It handles all user input and sends to the processor as necessary'''
	def __init__(self,processor,display):
		self.processor = processor
		self.display = display
#		readline.parse_and_bind('tab: complete')

	# Waits for input from the user, then sends it off to be handled
	def __running__(self):
		'''Our default running loop which governs the UI'''
		while True:
			chat = input('')
			self.decode(chat)

	# determines what to do with the string from wait_for_input
	def decode(self,message):
		'''Decode is responsible for breaking down and figuring what to do with the input line'''
		if message is "":
			return

		# User wants to connect to a specific ip:port pair
		if '/con ' in message[:5]:
			self.processor.send('connection',message[5:])
			return
		# User wants to whisper to an alias (if it exists)
		if '/w ' in message[:3]:
			target, whisper = self.split_target_and_message(message[3:])
			if target is not "":
				self.processor.whisper(whisper,target)
			return
		# User wants to reply to the most recent whisperer (if it exists)
		if '/r ' in message[:3]:
			self.processor.reply(message[3:])
			return
		# User wants to disconnect this node
		if '/exit' in message[:5]:
			self.processor.exit()
			return
		# User wants to ping its active serverlist
		if '/pingall' in message[:8]:
			self.processor.broadcast('ping')
			return
		# User wants a ping update from only a specific node
		if '/ping ' in message[:6]:
			self.processor.send('ping',message[6:])
			return
		# User wants to know more information about an alias or ipaddress
		if '/? ' in message[:3]:
			key = message[3:]
			self.processor.identity(key)
			return

		# User wants to know which aliases are active
		if '/who' in message[:4]:
			self.processor.who()
			return
		# User wants to know more about the application
		if '/about' in message[:6]:
			self.processor.about()
			return

		if '/import ' in message[:8]:
			self.processor.importNode(message[8:])
			return

		if '/export' in message[:7]:
			self.processor.exportSelf()
			self.display.info('Exported settings to file!')
			return

		# default: send a chat message
		self.processor.broadcast('chat',message)

	def split_target_and_message(self,message):
		'''This method attempts to split the alias/location and message in an input line'''
		if len(message) > 0:
			try:
				index_of_space = message.index(' ')
				return message[:index_of_space], message[index_of_space+1:]
			except:
				self.display.warn('Cannot send a whisper without a message.')
				return "",""
		self.display.warn('Improper target or message format.')
		return "",""
