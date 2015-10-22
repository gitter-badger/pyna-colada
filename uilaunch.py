import socket, sys
from pyna import *

try:
    # Get the local ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
    address = s.getsockname()[0]
    s.close()
except:
    address = "localhost"

# Grab cmdline args and config.json
if len(sys.argv) == 3:
    alias = sys.argv[1]
    port = sys.argv[2]
else:
    alias = input('Please enter an alias:  ')
    port = input('Please enter a port on which the server will listen (default=8080): ')
    if port is "":
        port = 8080

node = UINode(alias,address,port)

node.start()
