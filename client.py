import json, socket, sys
from datetime import datetime, timezone
from utility import color, color_print, utc_to_local

# Main client class
class PyNaClient(object):
    def __init__(self, location, alias):
        self.alias = alias
        self.active_server_list = []
        self.location = location
        self.active_aliases = {}
        self.most_recent_whisperer = ""

    # show a message on the client
    def display(self, msg):
        if msg['type'] == 'whisper':
            # Format this differently
            color_print("{0} <W>: {1}".format(msg['sender']['name'], msg['message']),color.blue)
            self.most_recent_whisperer = msg['sender']['name']
            return
        color_print("{0}: {1}".format(msg['sender']['name'], msg['message']),color.gray)

    def disconnect(self,sender):
        color_print("{0} ({1}) has disconnected".format(sender['name'],sender['location']),color.dark_gray)
        self.deactivate_server(sender['location'])


    # Try to activate the server, or at least the alias
    def activate_server(self, location, alias=""):
        if location not in self.active_server_list:
            self.active_server_list.append(location)
            self.connect_to(location)
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
            self.handle_request(chat)

    # determines what to do with the string from wait_for_input
    def handle_request(self,message):
        if message is "":
            return

        if '/c ' in message[:3]:
            self.connect_to(message[3:])
            return
        if '/w ' in message[:3]:
            index_of_space = 3 + message[3:].index(' ')
            alias = message[3:index_of_space]
            packed_json = self.package('whisper',message[index_of_space+1:])
            self.send_to_alias(alias,packed_json)
            return
        if 'r ' in message[:3]:
            packed_json = self.package('whisper',message[3:])
            self.send_to_alias(self.most_recent_whisperer,packed_json)
            return
        if '/x' in message[:2]:
            color_print('Closing down server. Thank you for using PyÑa Colada!',color.pyna_colada)
            close_message = self.package('disconnection')
            self.send_to_all(close_message)
            sys.exit(0)
            return
        if '/servers' in message[:8]:
            print(self.active_server_list)
            print()
            return
        if '/who' in message[:4]:
            print(list(self.active_aliases.keys()))
            print()
            return
        packed_json = self.package('chat',message)
        self.send_to_all(packed_json)

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
            color_print('No one hears you...',color.blue)

    # Try to send over socket
    def try_to_send(self, target, js, hide_output=False):
        if target == '{0}'.format(self.location):
            return
        address, port = target.split(':')
        #color_print('sending {0} message to {1}:{2}'.format(js['type'],address,port),color.green)
        message = str.encode(str(json.dumps(js)))
        total_sent = 0
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.settimeout(1.0)
            self.sock.connect((address,int(port)))
            while total_sent < len(message):
                sent = self.sock.send(message[total_sent:])
                if sent == 0:
                    raise RuntimeError('Connection closed erroneously')
                total_sent = total_sent + sent
            self.sock.close()
            self.activate_server(target)
        except Exception as msg:
            #color_print('{0}:{1} -- {2}'.format(address,port,msg),color.fail)
            if not hide_output:
                color_print('mesh-chat application does not appear to exist at {0}:{1}'.format(address,port),color.warn)
            self.deactivate_server(target)
