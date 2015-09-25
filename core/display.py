class Display(object):
	class color:
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
		print(printed_color + message + Display.color.end)

	# display a message received according to type
	def display(msg):
		sender_tag = msg['sender']['name']
		message = msg['message']
		sent_at = msg['time_sent']
		# If this is a whisper, format as blue
		if msg['type'] == 'whisper':
			Display.whisper(sender_tag,message)
			return
		Display.chat(sender_tag,message)

	def chat(sender_tag,message, chat_color=color.gray):
		sender_tag = Display.bold(sender_tag, [0,len(sender_tag)],chat_color)
		Display.color_print("{0}: {1}".format(sender_tag, message),chat_color)

	def whisper(sender_tag,message):
		sender_tag = sender_tag + ' <W>'
		Display.chat(sender_tag,message,Display.color.blue)

	def disconnected(alias, location):
		Display.info('{0} ({1}) has disconnected')

	# Logging methods
	def log(message):
		Display.color_print(message,Display.color.green)
	def debug(message):
		Display.color_print(message,Display.color.dark_gray)
	def warn(message):
		Display.color_print(message,Display.color.warn)
	def error(message):
		Display.color_print(message,Display.color.fail)
	def info(message):
		Display.color_print(message,Display.color.dark_gray)
	def server_announce(message):
		Display.color_print(message, Display.color.pyna_colada)

	# surrounds part of the message with tags that make it bold
	def bold(message, bold_range, color_after):
		# insert bold tag, end tag, and color_after
		bold_region = Display.color.bold + message[bold_range[0]:bold_range[1]] + Display.color.end + color_after
		return message[:bold_range[0]] + bold_region + message[bold_range[1]:]
