import socket, sys
from pyna.node.AutonomousNode import AutonomousNode

try:
    # Get the local ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
    address = s.getsockname()[0]
    s.close()
except:
    address = "localhost"

# Grab cmdline args and config.json
if len(sys.argv) == 2:
    alias = 'Autonomous'
    port = sys.argv[1]
else:
    port = input('Please enter a port on which the server will listen (default=8080): ')
    if port is "":
        port = 8080

node = AutonomousNode(alias,address,port)

node.start()
