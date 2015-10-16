import json, socket, sys, requests
from core.display import Display

# Main client class
class Sender(object):
    '''Socket Sender; responsible ONLY for sending messages on an anonymous port'''
    def __init__(self,display):
        self.active_server_list = []
        self.active_aliases = {}
        self.display = display

    # Try to send over socket
    def try_to_send(self, message,target):
        '''Wrapper for sending on a socket; boolean indicates successful send'''
        try:
            location, port = target.split(':')
        except ValueError as msg:
            self.display.warn("Value Error: {0}".format(msg))
            return False
        except AttributeError:
            self.display.debug('Sender ERROR: No user was found at {0}'.format(target))
        # encode the json and create the socket
        try:
            self.send(message,location,port)
        except Exception as msg:
            self.display.debug('Sender ERROR: {0}\n'.format(msg))
            return False
        return True

    def send(self,message,location,port):
        '''Actually send an encoded json message to the location and port'''
        try:
            r = requests.post('http://{0}:{1}'.format(location, port), json={"message":message},headers={'Connection':'close'}, stream=False, timeout=0.001)
            f = r.status_code # nope, don't worry about this
        except Exception as msg: pass
            #display.debug(msg)
