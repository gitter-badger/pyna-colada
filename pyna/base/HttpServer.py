import http.server, json

class HttpServer(http.server.BaseHTTPRequestHandler):
    def log_message(self,format,*args): pass
        # Keep quiet

    def do_POST(self):
        '''
        Actually handles the receipt of messages on the socket
        '''
        self.accept_POST()

    def accept_POST(self):
        '''Occurs when not Blacklisted'''
        # Get the data
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        self.send_response(200,"OK")
        self.end_headers()

        # Now, interpret
        self.server.interpretMessage(post_data)
