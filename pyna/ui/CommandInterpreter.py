from pyna.base.Interpreter import Interpreter
from pyna.core.Dispatcher import Dispatcher
from pyna.ui.PynaDisplay import PynaDisplay
import sys, time, json

class CommandInterpreter(Interpreter):
    def __init__(self, manager, dispatcher):
        self.manager = manager
        self.dispatcher = dispatcher

    def typed_about(self,ignore):
        PynaDisplay.splash(self.manager.version)

    def typed_exit(self,ignore):
        PynaDisplay.server_announce('Closing down node. Thank you for using PyÑa Colada!')
        self.dispatcher.broadcast('disconnection')
        time.sleep(0.5)
        sys.exit(0)

    def typed_whisper(self, remainder):
        try:
            target, message = remainder.split(' ',1)
        except:
            PynaDisplay.warn("Improperly formatted whisper command")
            return
        self.dispatcher.send('whisper',content=message, target=target)

    def typed_reply(self, message):
        self.dispatcher.send('whisper',content=message, target=self.manager.most_recent_whisperer)

    def typed_whisperlock(self, message):
        self.dispatcher.send('whisper',content=message, target=self.manager.whisper_lock_target)

    def typed_info(self,key): #TODO: Move to display
        user = self.manager.getNode(key)
        if user is None:
            PynaDisplay.info('No user or node was found with key \'{0}\''.format(key))
            return
        self.typed_identity(user)

    def typed_ping(self, target):
        self.dispatcher.send('ping', target=target)

    def typed_pingall(self, target):
        self.dispatcher.broadcast('ping')

    def typed_import(self, filename):
        '''Attempt to import a node file'''
        new_node = self.manager.node_list.importNode(filename)
        if new_node is None:
            PynaDisplay.warn('Malformed or missing file \'{0}\''.format(filename))
            return
        node_list = self.manager.get_node_list()
        self.dispatcher.send('nodelist', content=node_list, target=new_node)

    def typed_who(self, ignore):
        if len(self.manager.active_nodes) == 0:
            PynaDisplay.info('No nodes are active')
            return
        PynaDisplay.log('Active users')
        for node in self.manager.active_nodes:
            self.identity(node)

    def typed_chat(self,msg):
        self.dispatcher.broadcast('chat', content=msg)

    def typed_ban(self, remainder):
        try:
            target, message = remainder.split(' ',1)
        except:
            PynaDisplay.warn("Erroneous ban command: Please specify target and reason")
            return
        self.manager.addToBlackList(target,message)

    def typed_whispertoggle(self, remainder):
        target = remainder.split(' ',1)[0]
        self.manager.whisperToggle(target)

    # Helpful commands
    def identity(self,node):
        PynaDisplay.info("{2}:  {0} ({1})".format(node['alias'],node['uid'],node['location']))
