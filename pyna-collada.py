import json, socket, requests, threading, time, sys

class color:
    header = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    end = '\033[0m'

def color_print(message,printed_color):
    print(printed_color + message + color.end)



# Main client class
class PynaClient(object):
    def __init__(self, location, alias="anonymous"):
        self.alias = alias
        self.active_server_list = []
        self.location = location
        self.active_aliases = {}

    # show a message on the client
    def display(self, msg):
        if msg['type'] == 'whisper':
            # Format this differently
            color_print("{0} <W>: {1}".format(msg['sender']['name'], msg['message']),color.blue)
        color_print("{0}: {1}".format(msg['sender']['name'], msg['message']),color.header)

    # Try to activate the server, or at least the alias
    def activate_server(self, location, alias):
        if location not in self.active_server_list:
            self.active_server_list.append(location)
            color_print('ALERT: Activated {0}'.format(location),color.green)
            self.connect_to(location)
        if alias not in self.active_aliases:
            self.active_aliases[alias] = location
            color_print('ALERT: Registered {0} at {1}'.format(alias,location),color.green)

    # Package up our data. Most of this will be in a json file, but we're not quite there yet
    def package(self,message_type,message=""):
        data = {}
        data["type"] = message_type
        data["client"] = "Pyna colada"
        data["client_version"] = "v0.0.1"
        data["sender"] = {"name": self.alias, "location": self.location}
        data["message"] = message
        return data

    # Waits for input from the user, then sends it off to be handled
    def wait_for_input(self):
        while True:
            chat = input('{0}@{1}:  '.format(self.alias,self.location))
            client.handle_request(chat)

    # determines what to do with the string from wait_for_input
    def handle_request(self,message):
        if '/c ' in message[0:3]:
            self.connect_to(message[3:])
            return
        packed_json = self.package('chat',message)
        self.send_to_all(packed_json)

    def connect_to(self,location):
        connection_json = self.package('connection')
        self.try_to_send(location,connection_json)

    # Send JSON to all active servers
    def send_to_all(self,json):
        for active_server in self.active_server_list:
            self.try_to_send(active_server,json)

    # Send JSON to a whisper target
    def send_to_alias(self,target_alias,json):
        if target_alias in self.active_aliases:
            self.try_to_send(self.active_aliases[target_alias],json)

    # Try to send over socket
    def try_to_send(self, target, js):
        address, port = target.split(':')
        message = str.encode(str(json.dumps(js)))
        total_sent = 0
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((address,int(port)))
        while total_sent < len(message):
            sent = self.sock.send(message[total_sent:])
            if sent == 0:
                raise RuntimeError('Connection closed erroneously')
            total_sent = total_sent + sent
        self.sock.close()


# Main server clas
class PynaServer(object):
    def __init__(self, client, address='localhost',port=2008):
        self.authorized_server_list = []
        self.client = client
        self.address = address
        self.port = port

    # This is the big part where we are waiting for messages
    def listen(self):
        try:
            # Try to bind the socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.address, self.port))
            self.sock.listen(1)
            self.client.sock = self.sock
            color_print('Socket bound appropriately',color.green)
        except socket.error as msg:
            # No dice. Kill the process.
            self.sock = None
            color_print('Unable to bind socket: {0}'.format(msg),color.fail)
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
        if (msg['type'] == 'chat' or msg['type'] == 'whisper'):
            self.client.display(msg)
        if msg['type'] == 'connect':
            self.connect(msg['sender'])
        # Nonetheless, try to activate the server on the client
        self.client.activate_server(msg['sender']['location'],msg['sender']['name'])

    # For new connections
    def connect(self, sender):
        if sender['location'] not in self.authorized_server_list:
            self.authorized_server_list.append(sender['location'])




# Set up
alias = sys.argv[1]
address = sys.argv[2]
port = sys.argv[3]

client = PynaClient('{0}:{1}'.format(address,port),alias)
server = PynaServer(client,address,int(port))
server_thread = threading.Thread(target=server.listen)
server_thread.daemon = True
server_thread.start()

#Await initialization
time.sleep(1)
client_thread = threading.Thread(target=client.wait_for_input)
client_thread.start()
