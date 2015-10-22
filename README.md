#PyÑa Colada [![Code Climate](https://codeclimate.com/github/etkirsch/pyna-colada/badges/gpa.svg)](https://codeclimate.com/github/etkirsch/pyna-colada) [![Test Coverage](https://codeclimate.com/github/etkirsch/pyna-colada/badges/coverage.svg)](https://codeclimate.com/github/etkirsch/pyna-colada/coverage)
A `mesh-chat` application built in Python 3.4.3. PyÑa Colada uses combined RSA (PKCS1 1.5) and AES-256 encryption for sending and receiving messages. It is a nearly-fully-featured, fully-configurable chat client that can be run in a bash terminal. PyÑa Colada also implements a modularized architecture intended for easy substitions (e.g. replacing the UI portion with a neural network or custom python script for autonomy).


##Installation and Running
NOTE: To run PyÑa Colada, you need to have at least Python 3.4 installed on a Linux device.

Download this project as a Zip, then extract it to a folder of your choice.  In a terminal navigate to this folder and execute `pip3 install --requirements requirements.txt`. Then, in the same directory run `python3 uilaunch.py [alias] [port]` where `[alias]` is your desired user name and `[port]` is the port on which you wish the server to listen. You will get the following output verifying that the server is running correctly

```
	PyÑa Colada Server v#.#.#
	Server running on [ip-address]:[port]
```

On your first run of the application, all you need to do is connect (details as follows) and then send messages. After you have connected to another mesh-chat node, all you need to do is log in.

##Available Operations
Note: `[node]` means that the input can be any node identifier, be it a user alias, an ip:port pair, or a UID.

#### Bindings
With v0.6.0, configurable bindings were incorporated in PyÑa Colada. To change the command bindings (defaults as follows), open your `config/config.json` and change the bindings listed.

#### Chatting
* `/all` sends a chat to every active and authorized node.
* `/w [node] [message]` whispers a message to the the user at the specified node
* `/wt [node] [message]` as whisper, but locks the application in WhisperToggle mode with the designated node until the `/wt` command is executed without a node identifier (message is optional in both cases)
* `/r [message]` whispers a message to the most recent person to whisper to you

The operation of `[message]` without a command varies. The `/all` command is assumed by default, but switches to `/w [node]` if locked in whisper toggle.

#### Other Operations
* `/block [node]` blocks communication to and from a specified node; also blocks the node from pinging you
* `/block [ip-address]` blocks communication from any port at a given ip address
* `/who` returns a list of all aliases available to your current instance
* `/? [node]` returns all available information about an active alias
* `/ping [node]` pings a specific node; useful for checking to see if someone has crashed
* `/pingall` pings every authorized node as per your configuration settings
* `/about` provides information about the node you are running
* `/exit` disconnects from the mesh network and exits the application

## Node Types
* **UI** (accessible via the `uilaunch.py` script) launches a full-featured PyÑa Colada node with UI.
* **Autonomous** (accessible via the `autolaunch.py` script) launches a PyÑa Colada node without a UI component. To quit, simply type q in the terminal. This type is in development.
* **Base** (inaccessible) is an extremely basic PyÑa Colada node with no logic outside of encryption/sending and decryption/receiving. Intended for scripts and bots. Not available yet

##Future Features
* **Message Relays** which permit multi-network relaying of messages (coming in v0.7.0)
