import json, socket, time, sys,cgi,urllib
import http.server, socketserver

# Main server clas
class Listener(object):
    '''Http Server parent class; responsible for creating, binding, and listening'''

    def __init__(self, port, interpreter):
        self.port = port
        self.interpreter = interpreter

    def __launch__(self):
        '''Create and bind a socket on the location and port specified at startup'''
        try:
            Handler = PynaColadaHttpServer
            httpd = PynaColadaTCPServer(("",self.port), Handler, self.interpreter)
            httpd.serve_forever()
        except socket.error as msg:
            # No dice. Kill the process.
            print('ERROR: Unable to bind socket: {0}'.format(msg))
            sys.exit(0)

class PynaColadaTCPServer(socketserver.TCPServer):
    def __init__(self,location,handler,interpreter):
        super().__init__(location,handler)
        self.interpreter = interpreter

    def interpretMessage(self, msg):
        self.interpreter.interpretMessage(msg)

class PynaColadaHttpServer(http.server.BaseHTTPRequestHandler):
    # Keep quiet
    def log_message(self,format,*args): pass

    def do_POST(self):
        '''
        Actually handles the receipt of messages on the socket
        '''
        # Get the data and respond
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        self.send_response(200,"OK")
        self.end_headers()

        # Now, interpret
        self.server.interpretMessage(post_data)
