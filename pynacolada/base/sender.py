import json, socket, sys, requests,threading

class Sender(object):
    '''Socket Sender; responsible ONLY for sending messages on an anonymous port'''

    # Try to send over socket
    def try_to_send(self, message,target):
        '''
        Wrapper for sending on a socket; boolean indicates successful send
        '''
        location, port = target.split(':')
        sender_thread = threading.Thread(target=self.send,args=(message,location,port,))
        sender_thread.daemon = True
        sender_thread.start()
        return True

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
