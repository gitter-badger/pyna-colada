import socketserver
from pynacolada.core.interpreter import Interpreter

class UINodeTCPServer(socketserver.TCPServer):
    '''
    A TCP Server which sends to a core.Interpreter on POST
    '''

    def __init__(self,location,handler,interpreter):
        super().__init__(location,handler)
        self.interpreter = interpreter

    def interpretMessage(self, msg):
        self.interpreter.interpretMessage(msg)
