import json, socket, time, sys
from core.socketlistener import SocketListener
from display import Display
from packager import Packager

# Main server clas
class Listener(SocketListener):
    def __init__(self, alias, display, interpreter, address, port):
        super().__init__(address,port)
        self.interpreter = interpreter
        self.display = display

    # Same as super(), but includes notification and then tells the client to ping
    def create_socket(self):
        super().create_socket()
        if self.sock != None:
            self.interpreter.ping_all()
            self.display.log('Node running on {0}:{1}\n'.format(self.address,self.port))

    def interpret_message(self,msg):
        self.interpreter.interpret_message(msg)
