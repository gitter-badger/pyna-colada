import json, socket, time, sys,cgi,urllib

#TODO: FIX THIS -- BASE SHOULD NOT REFERENCE OUTSIDE OF BASE
from pynacolada.core.TCPServer import UINodeTCPServer
from pynacolada.core.HttpServer import UINodeHttpServer

# Main server clas
class Listener(object):
    '''Http Server parent class; responsible for creating, binding, and listening'''

    def __init__(self, port, interpreter):
        self.port = port
        self.interpreter = interpreter

    def __launch__(self):
        '''Create and bind a socket on the location and port specified at startup'''
        try:
            Handler = UINodeHttpServer
            httpd = UINodeTCPServer(("",self.port), Handler, self.interpreter)
            httpd.serve_forever()
        except socket.error as msg:
            # No dice. Kill the process.
            print('ERROR: Unable to bind socket: {0}'.format(msg))
            sys.exit(0)
