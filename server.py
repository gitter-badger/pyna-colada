import json, socket, time
from utility import color, color_print

# Main server clas
class PyNaServer(object):
    def __init__(self, client, address, port):
        self.server_config = json.load(open('config/config.json','r'))
        color_print('Welcome to PyÑa Colada Server v{0}'.format(self.server_config['serverVersion']),color.pyna_colada)
        self.authorized_server_list = []
        self.client = client
        self.address = address
        self.port = port
        self.load_servers()
        self.client.ping_all(self.authorized_server_list)

    # This is the big part where we are waiting for messages
    def listen(self):
        try:
            # Try to bind the socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.address, self.port))
            self.sock.listen(1)
            self.client.sock = self.sock
            color_print('Server running on {0}:{1}\n'.format(self.address,self.port),color.green)
        except socket.error as msg:
            # No dice. Kill the process.
            self.sock = None
            color_print('ERROR: Unable to bind socket: {0}'.format(msg),color.fail)
            return
        while self.sock is not None:
            # Now we wait
            self.receive()
            time.sleep(1)

    # Handles receipt of the actual json we take in
    def receive(self):
        connection, address = self.sock.accept()
        response = connection.recv(1024)
        msg = json.loads(response.decode("utf-8"))
        self.connect(msg['sender'])
        if (msg['type'] == 'chat' or msg['type'] == 'whisper'):
            self.client.display(msg)
        if msg['type'] == 'connection':
            self.connect(msg['sender'])
        if msg['type'] == 'disconnection':
            self.client.disconnect(msg['sender'])

    # For new connections
    def connect(self, sender):
        self.client.activate_server(sender['location'],sender['name'])
        if sender['location'] not in self.authorized_server_list:
            self.authorized_server_list.append(sender['location'])
            data = json.load(open('config/servers.json','r'))
            data.update({"servers":self.authorized_server_list})
            with open('config/servers.json','w') as auth:
                json.dump(data, auth)

    def load_servers(self):
        with open('config/servers.json','r') as auth:
            data = json.load(auth)
        for server in data['servers']:
            if server not in self.authorized_server_list:
                self.authorized_server_list.append(server)
