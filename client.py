import json, socket, sys
from datetime import datetime, timezone
from core.display import Display

# Main client class
class PyNaClient(object):
    def __init__(self, location, alias):
        self.alias = alias
        self.active_server_list = []
        self.location = location
        self.active_aliases = {}
        self.most_recent_whisperer = ""

    def utc_to_local(self,utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    # show a message on the client
    def display_message(self, msg):
        if msg['type'] == 'whisper':
            self.most_recent_whisperer = msg['sender']['name']
        Display.display(msg)

    # Notify user that a node has disconnected
    def disconnect_notify(self,sender):
        self.deactivate_server(sender['location'])
        Display.disconnected(sender['name'],sender['location'])

    # Try to add the alias/location to active servers and active aliases
    def activate_server(self, location, alias=""):
        if location not in self.active_server_list:
            self.active_server_list.append(location)
            self.send_serverlisthash(location)
        if alias is not "" and alias not in self.active_aliases:
            self.active_aliases[alias] = location
            Display.color_print('Registered {0} at {1}'.format(alias,location),Display.color.green)

    # remove an ip address (location) from active_server_list and its aliases
    def deactivate_server(self, location):
        if location in self.active_server_list:
            self.active_server_list.remove(location)
        if location in list(self.active_aliases.values()):
            self.active_aliases = {k:v for k,v in self.active_aliases.items() if v != location}

    # Package up our data. Most of this will be in a json file, but we're not quite there yet
    def create_message(self,message_type,message=""):
        data = {}
        data["type"] = message_type
        data['time_sent'] = self.utc_to_local(datetime.now(timezone.utc)).strftime("%Y-%m-%d %H:%M:%S")
        data["client"] = "Pyna colada"
        data["client_version"] = "v" + self.version
        data["sender"] = {"name": self.alias, "location": self.location, "uid": self.uid}
        data["message"] = message
        return data

    # Waits for input from the user, then sends it off to be handled
    def __running__(self):
        while True:
            chat = input('')
            self.handle_request(chat)

    # determines what to do with the string from wait_for_input
    def handle_request(self,message):
        if message is "":
            return

        # User wants to connect to a specific ip:port pair
        if '/c ' in message[:3]:
            connection_message = self.create_message('connection')
            location = message[3:]
            self.try_to_send(location,connection_message)
            return
        # User wants to whisper to an alias (if it exists)
        if '/w ' in message[:3]:
            if len(message) is 3:
                Display.warn('Cannot send a whisper without a target or message.')
                return
            try:
                index_of_space = 3 + message[3:].index(' ')
            except:
                Display.warn('Cannot send a whisper without a message.')
                return
            whisper_to_location = self.get_location(message[3:index_of_space])
            whisper_message = self.create_message('whisper',message[index_of_space+1:])
            self.try_to_send(whisper_to_location,whisper_message)
            return
        # User wants to reply to the most recent whisperer (if it exists)
        if '/r ' in message[:3]:
            whisper_message = self.create_message('whisper',message[3:])
            whisper_to_location = self.active_aliases[self.most_recent_whisperer]
            self.try_to_send(whisper_to_location,whisper_message)
            return
        # User wants to disconnect this node
        if '/x' in message[:2]:
            Display.server_announce('Closing down server. Thank you for using PyÑa Colada!')
            close_message = self.create_message('disconnection')
            self.send_to_all(close_message)
            sys.exit(0)
            return
        # User wants to ping its active serverlist
        if '/pingall' in message[:8]:
            packed_json = self.create_message('ping')
            self.send_to_all(packed_json)
            return
        # User wants a ping update from only a specific node
        if '/ping ' in message[:6]:
            packed_json = self.create_message('ping')
            location = self.get_location(message[6:])
            self.try_to_send(location,packed_json)
            return
        # User wants to know more information about an alias or ipaddress
        if '/? ' in message[:3]:
            key = message[3:]
            # if this is an alias
            if key in self.active_aliases:
                Display.info('User \'{0}\' at location {1}'.format(key,self.active_aliases[key]))
                return
            # if this is an ipaddress
            if key in self.active_server_list:
                # look for the corresponding alias for this address. Not pretty but it works
                if key in self.active_aliases.values():
                    for alias in self.active_aliases.items():
                        if alias[1] == key:
                            Display.info('User \'{0}\' at location {1}'.format(alias[0],key))
                            return
                # in case there is no known user alias
                Display.info('Unknown user at location {0}'.format(key))
                return
            # found nothing
            Display.info('No user or node was found with key \'{0}\''.format(key))
        # User wants to know what servers are active
        if '/servers' in message[:8]:
            print('Active servers:  {0}\n'.format(list(self.active_server_list)))
            return
        # User wants to know which aliases are active
        if '/who' in message[:4]:
            print('Active aliases:  {0}\n'.format(list(self.active_aliases.keys())))
            return
        # User wants to know more about the application
        if '/about' in message[:6]:
            Display.server_announce('\033[1mPyÑa Colada ' + Display.color.end + Display.color.pyna_colada + 'Node v' + self.version)
            Display.info('A mesh-chat type application written by Evan Kirsch (2015)\n')
            return

        # default: send a chat message
        packed_json = self.create_message('chat',message)
        self.send_to_all(packed_json)

    # Send a Connection message to a location
    def send_type_to_location(self,message_type,location):
        message = self.create_message(message_type)
        self.try_to_send(location,message)

    # Called by server to see which authorized servers are active
    def ping_all(self,authorized_server_list):
        ping_json = self.create_message('connection')
        for server in authorized_server_list:
            self.try_to_send(server,ping_json,hide_output=True)

    # Send JSON to all active servers
    def send_to_all(self,json):
        for active_server in self.active_server_list:
            self.try_to_send(active_server,json)

    # not sure if the user typed in a location or alias, so try to get a location
    def get_location(self,key):
        # if key is an alias
        if key in self.active_aliases:
            return self.active_aliases[key]

        # if key is a location
        if key in self.active_server_list:
            return key

    # dummy; sends a serverlist hash to a newly-connecting node
    def send_serverlisthash(self, target):
        slhash = self.create_message('serverlisthash')
        self.try_to_send(target, slhash)

    # Try to send over socket
    def try_to_send(self, target, js, hide_output=False):
        # Verify that we're not trying to send to ourself
        if target == '{0}'.format(self.location):
            return
        # Split the ipaddress and port
        try:
            address, port = target.split(':')
        except ValueError:
            Display.warn('ERROR: Port was not specified\n')
            return
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
            if js['type'] != 'connection':
                Display.warn('{2}... mesh-chat application does not appear to exist at {0}:{1}'.format(address,port,js['type']))
                self.deactivate_server(target)
            return
        # everything went according to plan, close the socket and activate the server
        self.sock.close()
        self.activate_server(target)
