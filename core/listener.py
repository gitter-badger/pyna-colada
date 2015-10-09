import json, socket, time, sys
from core.socketlistener import SocketListener

# Main server clas
class Listener(SocketListener):
    '''The listener which is actually used in PC; might have additional functionality soon'''
    def __init__(self, interpreter, location, port,debug=False):
        super().__init__(location,port,debug)
        self.interpreter = interpreter

    def interpret_message(self,msg):
        self.interpreter.interpret_message(msg)
