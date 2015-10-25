class Display(object):
	'''Anything which displays to the user should go through Display()'''

	class color:
		'''Collection of colors for color_print'''
		pyna_colada = '\033[93m'
		yellow = '\033[33m'
		gray = '\033[37m'
		dark_gray = '\033[90m'
		light_red = '\033[91m'
		green = '\033[92m'
		blue = '\033[94m'
		light_magenta = '\033[95m'
		light_cyan = '\033[96m'
		end = '\033[0m'

	class emphasis:
		default = '\033[49m'
		gray = '\033[1m'
		red = '\033[1;31m'
		yellow = '\033[1;33m'

	class background:
		red = "\033[41m"
		yellow = '\033[43m'

	def log(message):
		Display.color_print(message,Display.color.green)
	def debug(message):
		Display.color_print(message,Display.color.blue)
	def warn(message):
		Display.color_print(message,Display.color.yellow)
	def error(message):
		Display.color_print(message,Display.color.light_red)
	def info(message):
		Display.color_print(message,Display.color.light_cyan)
	def server_announce(message):
		Display.color_print(message, Display.color.pyna_colada)

	def color_print(message,printed_color='\033[37m'):
		'''Formats a message with a specific color (as Display.color)'''
		print('{0}{1}{2}'.format(printed_color, message, Display.color.end))

	def bold(message, color_after='\033[49m', bold_color='\033[1m'):
		# insert bold tag, end tag, and color_after
		return ''.join([bold_color, message, Display.color.end, color_after])
