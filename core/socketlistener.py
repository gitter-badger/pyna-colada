import json, socket, time, sys
from core.display import Display

# Main server clas
class SocketListener(object):
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def create_socket(self):
        # Create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Try to bind the socket
        try:
            self.sock.bind((self.address, self.port))
        except socket.error as msg:
            # No dice. Kill the process.
            Display.error('ERROR: Unable to bind socket: {0}'.format(msg))
            return
        # We have a working socket, set it up and inform the user
        self.sock.listen(1)
        self.client.sock = self.sock

    # Create a socket then log everything that we receive
    def __running__(self):
        self.create_socket()
        while self.sock is not None:
            msg = self.receive_from_socket()
            self.log(msg)
            time.sleep(1)

    # receive a message on our socket
    def receive_from_socket(self):
        connection, address = self.sock.accept()
        response = connection.recv(1024)
        return json.loads(response.decode("utf-8"))
