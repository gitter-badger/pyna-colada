class Display(object):
	'''Anything which displays to the user should go through Display()'''

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

	def color_print(message,printed_color):
		'''Formats a message with a specific color (as Display.color)'''
		print(printed_color + message + Display.color.end)

	def display(msg):
		'''Display a message received according to the type'''
		# Scrape out info
		sender_tag = msg['sender']['alias']
		message = msg['message']
		sent_at = msg['time_sent']
		# If this is a whisper, format as blue
		if msg['type'] == 'whisper':
			Display.whisper(sender_tag,message)
		# otherwise, if chat, format normally
		if msg['type'] == 'chat':
			Display.chat(sender_tag,message)

	def chat(sender_tag,message, chat_color=None):
		'''Display a message with formatting for chat; can be formatted with a specific color if desired'''
		if chat_color is None:
			chat_color = Display.color.gray
		sender_tag = Display.bold(sender_tag,chat_color)
		Display.color_print("{0}: {1}".format(sender_tag, message),chat_color)

	def whisper(sender_tag,message):
		'''Display a chat message in clue with the <W> tag attached'''
		sender_tag = sender_tag + ' <W>'
		Display.chat(sender_tag,message,Display.color.blue)

	def disconnected(alias, location):
		'''Inform the user that someone has disconnected'''
		Display.info('{0} ({1}) has disconnected'.format(alias,location))

	def log(message):
		Display.color_print(message,Display.color.green)
	def debug(message):
		Display.color_print(message,Display.color.blue)
	def warn(message):
		Display.color_print(message,Display.color.warn)
	def error(message):
		Display.color_print(message,Display.color.fail)
	def info(message):
		Display.color_print(message,Display.color.dark_gray)
	def server_announce(message):
		Display.color_print(message, Display.color.pyna_colada)

	# surrounds part of the message with tags that make it bold
	def bold(message, color_after):
		# insert bold tag, end tag, and color_after
		return Display.color.bold + message + Display.color.end + color_after
