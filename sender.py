import json, socket, sys
from display import Display
from packager import Packager

# Main client class
class Sender(object):
    def __init__(self,display):
        self.active_server_list = []
        self.active_aliases = {}
        self.display = display

    # Try to send over socket
    def try_to_send(self, target, js):
        try:
            address, port = target.split(':')
        except ValueError:
            self.display.warn('ERROR: Port was not specified\n')
            return False
        except AttributeError:
            self.display.warn('ERROR: No user was found at this port')
        # encode the json and create the socket
        message = str.encode(str(json.dumps(js)))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1.0)
        # try to connect and send on this socket
        try:
            total_sent = 0
            self.sock.connect((address,int(port)))
            while total_sent < len(message):
                sent = self.sock.send(message[total_sent:])
                if sent == 0:
                    raise RuntimeError('Connection closed erroneously')
                total_sent = total_sent + sent
        except Exception as msg:
            #self.display.warn('ERROR: \n')
            return False
        # everything went according to plan, close the socket and activate the server
        self.sock.close()
        return True
