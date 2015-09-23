#PyÑa Colada
A `mesh-chat` application built in Python 3.4.3

##Installation and Running
NOTE: To run PyÑa Colada, you need to have at least Python 3.4 installed on a Linux device.

Download this project as a Zip, then extract it to a folder of your choice. In a terminal navicate to this folder and execute `python3 pyna-colada.py [alias] [port]` where `[alias]` is your desired user name and `[port]` is the port on which you wish the server to listen. You will get the following output verifying that the server is running correctly

```
	PyÑa Colada Server v#.#.#
	Server running on [ip-address]:[port]
```

From here, all you need to do is connect (details as follows) and then send messages.

##Available Operations
* `[message]` sends a message to all activated servers
* `/c [ip-address]:[port]` connects to another mesh-chat server
* `/w [alias] [message]` whispers a message to the user with specified alias, if it exists
* `/servers` returns a list of all servers connected in the mesh network
* `/who` returns a list of all aliases available to your current instance
* `/x` shuts this mesh-chat server down

##Future Features
* Authorization of servers
* Serverlist sharing
