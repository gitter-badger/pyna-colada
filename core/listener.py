import json, socket, time, sys
from core.socketlistener import SocketListener

# Main server clas
class Listener(SocketListener):
    def __init__(self, interpreter, address, port):
        super().__init__(address,port)
        self.interpreter = interpreter

    def interpret_message(self,msg):
        self.interpreter.interpret_message(msg)
