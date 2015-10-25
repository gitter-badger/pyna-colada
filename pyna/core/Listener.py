import socket, sys
from pyna.base.TCPServer import TCPServer
from pyna.base.HttpServer import HttpServer
from pyna.base.Display import Display

class Listener(object):
    '''
    Http Server parent class; responsible for creating, binding, and listening
    '''

    def __init__(self, crypto, parser=None):
        self.crypto = crypto
        self.parser = parser
        self.handler_type = HttpServer
        self.server_type = TCPServer

    def attachParser(self, parser):
        self.parser = parser

    def __launch__(self, port):
        '''
        Daemonized; Create and bind a socket on the location and port specified at startup
        '''
        try:
            self.server_type.allow_reuse_address = True
            httpd = self.server_type(("",port), self.handler_type, self)
            httpd.serve_forever()

        # No dice. Kill the process.
        except socket.error as msg:
            Display.warn('ERROR: Unable to bind socket: {0}'.format(msg))


    def interpret(self, encrypted):
        '''
        Received a message from the TCP Server, so relay it to our message_interpreter
        '''
        try:
            decrypted = self.crypto.decrypt(encrypted)
        except Exception as msg:
            Display.warn('Warning: General decryption failure\n\n{0}'.format(msg))
            return

        #Display.debug(decrypted)
        if self.parser is not None:
            self.parser.handleMessage(decrypted)
