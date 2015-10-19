import socketserver

class TCPServer(socketserver.TCPServer):
    '''
    A TCP Server which sends to a core.Interpreter on POST
    '''

    def __init__(self,location,handler,interpreter):
        super().__init__(location,handler)
        self.interpreter = interpreter

    def interpretMessage(self, msg):
        self.interpreter.interpret(msg)
