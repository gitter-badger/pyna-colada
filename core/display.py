class Display(object):
	'''Anything which displays to the user should go through Display()'''

	def __init__(self,debug=False):
		self.debug_mode = debug


	class color:
		'''Collection of colors for color_print'''
		header = '\033[96m'
		blue = '\033[94m'
		green = '\033[92m'
		gray = '\033[37m'
		dark_gray = '\033[90m'
		pyna_colada = '\033[93m'
		warn = '\033[33m'
		fail = '\033[91m'
		end = '\033[0m'
		bold = '\033[1m'

	def color_print(self,message,printed_color):
		'''Formats a message with a specific color (as Display.color)'''
		print(printed_color + message + self.color.end)

	def display(self,msg):
		'''Display a message received according to the type'''
		# Scrape out info
		sender_tag = msg['sender']['alias']
		message = msg['message']
		sent_at = msg['time_sent']
		# If this is a whisper, format as blue
		if msg['type'] == 'whisper':
			self.whisper(sender_tag,message)
		# otherwise, if chat, format normally
		if msg['type'] == 'chat':
			self.chat(sender_tag,message)

	def chat(self, sender_tag,message, chat_color=color.gray):
		'''Display a message with formatting for chat; can be formatted with a specific color if desired'''
		sender_tag = self.bold(sender_tag,chat_color)
		self.color_print("{0}: {1}".format(sender_tag, message),chat_color)

	def whisper(self, sender_tag,message):
		'''Display a chat message in clue with the <W> tag attached'''
		sender_tag = sender_tag + ' <W>'
		self.chat(sender_tag,message,Display.color.blue)

	def disconnected(self, alias, location):
		'''Inform the user that someone has disconnected'''
		self.info('{0} ({1}) has disconnected'.format(alias,location))

	def log(self, message):
		self.color_print(message,self.color.green)
	def debug(self, message):
		if self.debug_mode:
			self.color_print(message,self.color.blue)
	def warn(self, message):
		self.color_print(message,self.color.warn)
	def error(self, message):
		self.color_print(message,self.color.fail)
	def info(self, message):
		self.color_print(message,self.color.dark_gray)
	def server_announce(self, message):
		self.color_print(message, self.color.pyna_colada)

	# surrounds part of the message with tags that make it bold
	def bold(self,message, color_after):
		# insert bold tag, end tag, and color_after
		return self.color.bold + message + self.color.end + color_after

	def pyna_colada(self, version):
		name = self.bold('PyÑa Colada', self.color.pyna_colada)
		self.server_announce('{0} Node v{1}'.format(name, version))
