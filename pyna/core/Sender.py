import json, socket, sys, requests,threading
from pyna.base.Display import Display

class Sender(object):
    '''Socket Sender; responsible ONLY for sending messages on an anonymous port'''

    def __init__(self, crypto):
        self.crypto = crypto

    # Try to send over socket
    def try_to_send(self, message, target_node):
        '''
        Wrapper for sending on a socket; boolean indicates successful send
        Argument "target_node" MUST be a node
        '''
        # Gather the target's location and port
        location, port = target_node['location'].split(':')

        # Encrypt
        publicKey = target_node['publicKey']
        encrypted = self.crypto.encrypt(message, publicKey)

        # Spin up a thread for the POST to occur
        sender_thread = threading.Thread(target=self.send,args=(encrypted,location,port,))
        sender_thread.daemon = True
        sender_thread.start()

    def send(self,message,location,port):
        '''
        Actually send an encoded json message to the location and port
        '''
        try:
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json', "Connection": "close"}
            with requests.Session() as s:
                payload = {"message" : message}
                url = 'http://{0}:{1}'.format(location, port)
                r = requests.post(url, json=payload, headers=headers, timeout=1.0)

        except: pass
