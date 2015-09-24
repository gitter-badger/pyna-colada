import json, socket, time, sys
from utility import color, color_print

# Main server clas
class PyNaServer(object):
    def __init__(self, client, address, port):
        self.authorized_server_list = []
        self.client = client
        self.address = address
        self.port = port
        self.server_config = json.load(open('config/config.json','r'))
        color_print('Welcome to \033[1mPyÑa Colada' + color.end + color.pyna_colada +' Server v{0}'.format(self.server_config['serverVersion']),color.pyna_colada)
        self.client.version = self.server_config['clientVersion']
        self.client.uid = self.server_config['uid']
        self.load_in_servers()

    # This is the big part where we are waiting for messages
    def __running__(self):
        # Create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Try to bind the socket
        try:
            self.sock.bind((self.address, self.port))
        except socket.error as msg:
            # No dice. Kill the process.
            self.sock = None
            color_print('ERROR: Unable to bind socket: {0}'.format(msg),color.fail)
            return
        # We have a working socket, set it up and inform the user
        self.sock.listen(1)
        self.client.sock = self.sock
        color_print('Server running on {0}:{1}\n'.format(self.address,self.port),color.green)
        # Ask the client to ping all servers
        self.client.ping_all(self.authorized_server_list)
        while self.sock is not None:
            # Now we wait
            self.receive()
            time.sleep(1)

    # Handles receipt of the actual json we take in
    def receive(self):
        # actually receive the message
        connection, address = self.sock.accept()
        response = connection.recv(1024)
        msg = json.loads(response.decode("utf-8"))
        # add this server to our list since we know it's real
        self.connect(msg['sender'])
        # Determine what needs to be done according to the message type
        if (msg['type'] == 'chat' or msg['type'] == 'whisper'):
            self.client.display_message(msg)
        if msg['type'] == 'disconnection':
            self.client.disconnect_notify(msg['sender'])
        if msg['type'] == 'ping':
            self.client.send_type_to_location('pingreply',msg['sender']['location'])

    # For new connections
    def connect(self, sender):
        # tell the client to try to activate the server
        self.client.activate_server(sender['location'],sender['name'])
        # Check to see if it is in our authorized_server_list, add it if not
        if sender['location'] not in self.authorized_server_list:
            self.authorized_server_list.append(sender['location'])
            # Update our servers.json with the new server info
            data = json.load(open('config/servers.json','r'))
            data.update({"servers":self.authorized_server_list})
            with open('config/servers.json','w') as auth:
                json.dump(data, auth)

    # Load the servers in out servers.json file into authorized_server_list
    def load_in_servers(self):
        # open the json
        with open('config/servers.json','r') as auth:
            data = json.load(auth)
        # add those which are not already in our authorized_server_list
        for server in data['servers']:
            if server not in self.authorized_server_list:
                self.authorized_server_list.append(server)
