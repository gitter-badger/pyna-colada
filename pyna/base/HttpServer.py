import http.server, json

class HttpServer(http.server.BaseHTTPRequestHandler):
    def log_message(self,format,*args): pass
        # Keep quiet

    def do_POST(self):
        '''
        Actually handles the receipt of messages on the socket
        '''
        if self.isNotBlackListed():
            self.accept_POST()


    def isNotBlackListed(self):
        # Check to see if Blacklist has been loaded, and load if not
        if not hasattr(self,'blacklist'):
            with open('config/blacklist.json','r') as blacklist:
                self.blacklist = json.load(blacklist)

        # Check to see if the Host header is in our blacklist
        return not any([y for y in self.blacklist if self.client_address[0] in y])


    def accept_POST(self):
        '''Occurs when not Blacklisted'''
        # Get the data
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        self.send_response(200,"OK")
        self.end_headers()

        # Now, interpret
        self.server.interpretMessage(post_data)
