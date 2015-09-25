import json, socket, time, sys
from server import SocketListener

# Main server clas
class PyNaServer(SocketListener):
    def __init__(self, client, address, port):
        super().__init__(address,port)
        self.authorized_server_list = []
        self.client = client
        self.server_config = json.load(open('config/config.json','r'))
        self.log('Welcome to \033[1mPyÑa Colada' + self.color.end + self.color.pyna_colada +' Server v{0}'.format(self.server_config['serverVersion']))
        self.client.version = self.server_config['clientVersion']
        self.client.uid = self.server_config['uid']
        self.load_in_servers()

    # Same as super(), but includes notification and then tells the client to ping
    def __running__(self):
        super().create_socket()
        if self.sock != None:
            # Ask the client to ping all servers, then notify the user that we're running
            self.client.ping_all(self.authorized_server_list)
            self.log('Server running on {0}:{1}\n'.format(self.address,self.port))
        while self.sock is not None:
            protocol_msg = self.receive_from_socket()
            self.interpret_message(protocol_msg)
            time.sleep(1)

    # Handles receipt of the actual json we take in
    def interpret_message(self,msg):
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
