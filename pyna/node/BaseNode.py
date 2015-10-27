from pyna.base.Crypto import Crypto
from pyna.core.Dispatcher import Dispatcher
from pyna.core.Listener import Listener
from pyna.core.Manager import Manager
from pyna.core.Sender import Sender

import json, threading, time

class BaseNode(object):
    '''Bare-bones node, contains no logic... just endpoints'''

    def __init__(self,alias,location,port):
        self.location = location
        self.port = port
        self.alias = alias
        self.manager = Manager(alias,location,port)

    def initialize(self):
        ''' Create Base Components'''
        self.crypto = self.manager.crypto
        self.listener = Listener(self.crypto)
        self.sender = Sender(self.crypto)
        self.dispatcher = Dispatcher(self.manager, self.sender)


    def start_up_listener(self):
        '''Set up the listener thread separately'''
        listener_thread = threading.Thread(target=self.listener.__launch__, args=(int(self.port),))
        listener_thread.daemon = True
        listener_thread.start()


    def export(self):
        '''Export the JSON containing all pertinent information about this node'''
        data = {"uid": self.manager.uid, "alias": self.alias, "location": ':'.join([self.location,self.port])}
        data["publicKey"] = self.manager.crypto.getPublic().decode('utf-8')

        # Add into Nodelist
        self.manager.node_list.add(data)

        with open('{0}.json'.format(self.alias),'w') as auth:
            json.dump(data, auth)


    def start(self):
        '''Start up this node'''
        self.initialize()
        self.start_up_listener()
        self.export()

        #Send a default ping
        self.dispatcher.broadcast('ping',targets=self.manager.node_list.authorized_nodes)
        self.__running__()


    def __running__(self):
        '''What happens directly after the listener starts; to be implemented by the user'''
        pass
