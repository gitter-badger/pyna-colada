import json, socket, time, sys
from core.socketlistener import SocketListener

# Main server clas
class Listener(SocketListener):
    def __init__(self, interpreter, address, port,debug=False):
        super().__init__(address,port,debug)
        self.interpreter = interpreter

    def interpret_message(self,msg):
        self.interpreter.interpret_message(msg)
