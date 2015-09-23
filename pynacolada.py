import socket, threading, sys, time
from server import PyNaServer
from client import PyNaClient

# Get the local ip address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
address = s.getsockname()[0]
s.close()

# Grab cmdline args and config.json
if len(sys.argv) == 3:
    alias = sys.argv[1]
    port = sys.argv[2]
else:
    alias = input('Please enter an alias:  ')
    port = input('Please enter a port on which the server will listen (default=8080): ')
    if port is "":
        port = 8080


# Build the client
client = PyNaClient('{0}:{1}'.format(address,port),alias)

# start the server up
server = PyNaServer(client,address,int(port))
server_thread = threading.Thread(target=server.listen)
server_thread.daemon = True
server_thread.start()


# Await initialization before starting client thread
time.sleep(1)
client_thread = threading.Thread(target=client.wait_for_input)
client_thread.start()
