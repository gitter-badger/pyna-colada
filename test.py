from pyna.ui.CommandLineInterface import CommandLineInterface
from pyna.base.Crypto import Crypto
from pyna.base.Sender import Sender
from pyna.core.Manager import Manager
from pyna.core.Dispatcher import Dispatcher

from pyna.server.MessageParser import MessageParser
from pyna.ui.CommandLineInterface import CommandLineInterface

class Tester(object):
    def __init__(self):
        manager = Manager('etk','localhost',8080)
        crypto = Crypto(manager.uid)
        sender = Sender(crypto)
        dispatcher = Dispatcher(manager,sender)

        self.cli = CommandLineInterface(manager,dispatcher)
        self.parser = MessageParser(manager, dispatcher)

    def tryUI(self):
        self.cli.__running__()

    def tryServer(self,type):
        test = {'sender': {'alias': 'ohno', 'location': 'localhost'},'type': type ,'message': 'Generic Message', 'client': 'Pyna colada'}
        self.parser.handleMessage(test)
