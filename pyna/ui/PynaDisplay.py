from pyna.base.Display import Display
import os

class PynaDisplay(Display):
    def display(msg):
        '''Display a chat message received according to the type'''
        # Scrape out info
        sender_tag = msg['sender']['alias']
        message = msg['message']

        # If this is a whisper, format as blue
        if msg['type'] == 'whisper':
            PynaDisplay.whisper(sender_tag,message)

        # otherwise, if chat, format normally
        if msg['type'] == 'chat':
            #os.system("notify-send '{1}' '{0}'".format(message,sender_tag))
            client_bold = PynaDisplay.getClientSpecificBold(msg['client'])
            PynaDisplay.chat(sender_tag,message, bold_color=client_bold)

    def getClientSpecificBold(client):
        '''Colors the bold from a person based on their client type'''
        if client == "Pyna colada":
            return PynaDisplay.emphasis.yellow
        if client == "Spiced Rumby":
            return PynaDisplay.emphasis.red
        return PynaDisplay.emphasis.gray

    def chat(sender_tag,message, chat_color='\033[37m', bold_color='\033[1m'):
        '''Display a message with formatting for chat; can be formatted with a specific color if desired'''

        sender_tag = PynaDisplay.bold(sender_tag,chat_color,bold_color=bold_color)
        PynaDisplay.color_print("{0}: {1}".format(sender_tag, message),chat_color)

    def whisper(sender_tag,message):
        '''Display a chat message in clue with the <W> tag attached'''
        sender_tag = sender_tag + ' <W>'
        PynaDisplay.chat(sender_tag,message,PynaDisplay.color.blue)

    def disconnected(sender):
        '''Inform the user that someone has disconnected'''
        PynaDisplay.info('{0} ({1}) has disconnected'.format(sender['alias'],sender['uid']))

    def splash(version):
        bold_name = PynaDisplay.bold('PyÑa Colada', PynaDisplay.color.pyna_colada)
        PynaDisplay.server_announce('{0} Node v{1}'.format(bold_name, version))
        PynaDisplay.info('A mesh-chat type application written by Evan Kirsch (2015)\n')
