import json, socket, sys
from core.display import Display

# Main client class
class Sender(object):
    '''Socket Sender; responsible ONLY for sending messages on an anonymous port'''
    def __init__(self,display):
        self.active_server_list = []
        self.active_aliases = {}
        self.display = display

    # Try to send over socket
    def try_to_send(self, js,target):
        '''Wrapper for sending on a socket; boolean indicates successful send'''
        try:
            address, port = target.split(':')
        except ValueError as msg:
            self.display.warn(msg)
            return False
        except AttributeError:
            self.display.debug('ERROR: No user was found at {0}'.format(target))
        # encode the json and create the socket
        message = str.encode(str(json.dumps(js)))
        try:
            self.socket_send(message,address,port)
        except Exception as msg:
            self.display.debug('ERROR: {0}\n'.format(msg))
            return False
        return True

    def socket_send(self,message,address,port):
        '''Actually send an encoded json message to the address and port'''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1.0)
        # try to connect and send on this socket
        total_sent = 0
        self.sock.connect((address,int(port)))
        # Loop while we send a stream
        while total_sent < len(message):
            sent = self.sock.send(message[total_sent:])
            if sent == 0:
                raise RuntimeError('Connection closed erroneously')
            total_sent = total_sent + sent
        # everything went according to plan, close the socket and activate the server
        self.sock.close()
