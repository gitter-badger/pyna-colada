import json, socket, requests, threading, time, sys
from datetime import datetime, timezone

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

class color:
    header = '\033[96m'
    blue = '\033[94m'
    green = '\033[92m'
    gray = '\033[37m'
    pyna_colada = '\033[93m'
    warn = '\033[33m'
    fail = '\033[91m'
    end = '\033[0m'

def color_print(message,printed_color):
    print(printed_color + message + color.end)



# Main client class
class PynaClient(object):
    def __init__(self, location, alias):
        self.alias = alias
        self.active_server_list = []
        self.location = location
        self.active_aliases = {}

    # show a message on the client
    def display(self, msg):
        if msg['type'] == 'whisper':
            # Format this differently
            color_print("{0} <W>: {1}".format(msg['sender']['name'], msg['message']),color.blue)
            return
        color_print("{0}: {1}".format(msg['sender']['name'], msg['message']),color.gray)

    # Try to activate the server, or at least the alias
    def activate_server(self, location, alias=""):
        if location not in self.active_server_list:
            self.active_server_list.append(location)
        if alias is not "" and alias not in self.active_aliases:
            self.active_aliases[alias] = location
            color_print('Registered {0} at {1}'.format(alias,location),color.green)

    def deactivate_server(self, location):
        if location in self.active_server_list:
            self.active_server_list.remove(location)
        if location in list(self.active_aliases.values()):
            self.active_aliases = {k:v for k,v in self.active_aliases.items() if v != location}

    # Package up our data. Most of this will be in a json file, but we're not quite there yet
    def package(self,message_type,message=""):
        data = {}
        data["type"] = message_type
        data['time_sent'] = utc_to_local(datetime.now(timezone.utc)).strftime("%Y-%m-%d %H:%M:%S")
        data["client"] = "Pyna colada"
        data["client_version"] = "v0.0.1"
        data["sender"] = {"name": self.alias, "location": self.location}
        data["message"] = message
        return data

    # Waits for input from the user, then sends it off to be handled
    def wait_for_input(self):
        while True:
            chat = input('')
            client.handle_request(chat)

    # determines what to do with the string from wait_for_input
    def handle_request(self,message):
        try:
            if '/c ' in message[0:3]:
                self.connect_to(message[3:])
                return
            if '/w ' in message[0:3]:
                index_of_space = 3 + message[3:].index(' ')
                alias = message[3:index_of_space]
                packed_json = self.package('whisper',message[index_of_space+1:])
                self.send_to_alias(alias,packed_json)
                return
            packed_json = self.package('chat',message)
            self.send_to_all(packed_json)
        except:
            color_print('Please format your request appropriately',color.warn)

    def connect_to(self,location):
        connection_json = self.package('connection')
        self.try_to_send(location,connection_json)

    # Called by server to see which authorized servers are active
    def ping_all(self,authorized_server_list):
        ping_json = self.package('connection')
        for server in authorized_server_list:
            self.try_to_send(server,ping_json,hide_output=True)

    # Send JSON to all active servers
    def send_to_all(self,json):
        for active_server in self.active_server_list:
            self.try_to_send(active_server,json)

    # Send JSON to a whisper target
    def send_to_alias(self,target_alias,json):
        if target_alias in self.active_aliases:
            self.try_to_send(self.active_aliases[target_alias],json)
        else:
            printed_color('No one hears you...',color.blue)

    # Try to send over socket
    def try_to_send(self, target, js, hide_output=False):
        if target == '{0}'.format(self.location):
            return
        address, port = target.split(':')
        message = str.encode(str(json.dumps(js)))
        total_sent = 0
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.connect((address,int(port)))
            while total_sent < len(message):
                sent = self.sock.send(message[total_sent:])
                if sent == 0:
                    raise RuntimeError('Connection closed erroneously')
                total_sent = total_sent + sent
            self.sock.close()
            #color_print('{0} message sent to {1}:{2} successfully'.format(js['type'],address,port),color.green)
            self.activate_server(target)
        except Exception as msg:
            #color_print('{0}:{1} -- {2}'.format(address,port,msg),color.fail)
            if not hide_output:
                color_print('mesh-chat application does not appear to exist at {0}:{1}'.format(address,port),color.warn)
            self.deactivate_server(target)


# Main server clas
class PynaServer(object):
    def __init__(self, client, address, port):
        self.server_config = json.load(open('serverconfig.json','r'))
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
        # Nonetheless, try to activate the server on the client

    # For new connections
    def connect(self, sender):
        self.client.activate_server(sender['location'],sender['name'])
        if sender['location'] not in self.authorized_server_list:
            self.authorized_server_list.append(sender['location'])
            with open('authorizedservers.json','r') as auth:
                data = json.load(auth)
            data.update({"servers":self.authorized_server_list})
            with open('authorizedservers.json','w') as auth:
                json.dump(data, auth)

    def load_servers(self):
        with open('authorizedservers.json','r') as auth:
            data = json.load(auth)
        for server in data['servers']:
            if server not in self.authorized_server_list:
                self.authorized_server_list.append(server)


# Get the local ip address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
address = s.getsockname()[0]
s.close()

# Grab cmdline args and config.json
alias = sys.argv[1]
port = sys.argv[2]

# Build the client
client = PynaClient('{0}:{1}'.format(address,port),alias)

# start the server up
server = PynaServer(client,address,int(port))
server_thread = threading.Thread(target=server.listen)
server_thread.daemon = True
server_thread.start()

# Await initialization before starting client thread
time.sleep(1)
client_thread = threading.Thread(target=client.wait_for_input)
client_thread.start()
