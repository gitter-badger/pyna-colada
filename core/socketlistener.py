import json, socket, time, sys

# Main server clas
class SocketListener(object):
    '''Socket Listening parent class; responsible for creating, binding, and listening on a socket'''

    def __init__(self, location, port, debug=False):
        self.location = location
        self.port = port
        self.debug = debug

    def create_socket(self):
        '''Create and bind a socket on the location and port specified at startup'''
        # Create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Try to bind the socket
        try:
            self.sock.bind((self.location, self.port))
        except socket.error as msg:
            # No dice. Kill the process.
            print('ERROR: Unable to bind socket: {0}'.format(msg))
            return
        # We have a working socket, listen on it with a 1.0s time out
        self.sock.listen(1.0)

    # Create a socket then log everything that we receive
    def __running__(self):
        '''Listening loop'''
        self.create_socket()
        while self.sock is not None:
            self.receive_from_socket()
            time.sleep(1.0)

    # do something with the message we have received
    def interpret_message(self,msg):
        '''interpret the received message; override this method'''
        pass

    # receive a message on our socket
    def receive_from_socket(self):
        '''Actually handles the receipt of messages on the socket'''
        connection, location = self.sock.accept()
        response = connection.recv(65535)
        self.interpret_message(response)
