import socket, sys
from pynacolada.base.TCPServer import TCPServer
from pynacolada.base.HttpServer import HttpServer
from pynacolada.base.display import Display

class Listener(object):
    '''
    Http Server parent class; responsible for creating, binding, and listening
    '''

    def __init__(self, crypto, message_interpreter):
        self.crypto = crypto
        self.message_interpreter = message_interpreter

    def __launch__(self, port):
        '''
        Daemonized; Create and bind a socket on the location and port specified at startup
        '''
        try:
            Handler = HttpServer
            httpd = TCPServer(("",port), Handler, self)
            httpd.serve_forever()
        except socket.error as msg:
            # No dice. Kill the process.
            Display.warn('ERROR: Unable to bind socket: {0}'.format(msg))
            sys.exit(0)

    def interpret(self, encrypted):
        '''
        Received a message from the TCP Server, so relay it to our message_interpreter
        '''
        decrypted = self.crypto.decrypt(encrypted)
        self.message_interpreter.interpret(decrypted)
