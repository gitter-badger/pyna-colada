from pyna.base.HttpServer import HttpServer
import http.server, json

class PynaHttpServer(HttpServer):

    def do_POST(self):
        '''
        Actually handles the receipt of messages on the socket
        '''
        if self.isNotBlackListed():
            self.accept_POST()


    def isNotBlackListed(self):
        # Check to see if Blacklist has been loaded, and load if not
        if not hasattr(self,'blacklist'):
            return True

        # Check to see if the Host header is in our blacklist
        return not any([y for y in self.blacklist if self.client_address[0] in y])
