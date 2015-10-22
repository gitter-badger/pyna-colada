import hashlib, json, os, string, random
from pyna.core.Packager import Packager
from pyna.core.NodeList import NodeList
from pyna.ui.PynaDisplay import PynaDisplay

class Manager(object):
	'''
	Manages all things related to other nodes and configuration settings
	'''

	def __init__(self, alias, location, port):
		self.alias = alias
		self.active_nodes = []
		self.most_recent_whisperer = None
		self.location = '{0}:{1}'.format(location,port)
		self.node_list = NodeList()
		self.load()

	def load(self):
		'''
		Load all configuration settings and nodes
		'''
		if not os.path.isfile('config/config.json'):
			self.createConfig()
		config = json.load(open('config/config.json','r'))

		self.version = config['version']
		self.getUid()
		self.node_list.load()

	def getBindings(self):
		config = json.load(open('config/config.json','r'))
		return config['bindings']

	def getUid(self):
		'''Load UID from users.json or create it'''
		users = json.load(open('config/users.json','r'))
		try:
			self.uid = users[self.alias]
		except Exception as msg:
			self.uid = self.generateUid(32)
			PynaDisplay.warn('Generated New UID: {0}'.format(self.uid))
			users[self.alias] = self.uid
			with open('config/users.json','w') as out:
				json.dump(users, out)

	def generateUid(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for x in range(size))

	def createConfig(self):
		data = {"version": "0.5.0","name": "Py\u00d1a Colada","users": []}
		with open('config/config.json','w') as config:
			json.dump(data, config)

	def getPackager(self):
		'''
		Create a packager from our config settings
		'''
		return Packager(self.version,{"alias": self.alias, "location": self.location, "uid": self.uid})

	def getNode(self, key):
		if type(key) is not dict:
			key = self.node_list.find(key)
		else:
			 key = self.node_list.matchTo(key)

		if (key is None or key['location'] == self.location):
			return None

		return key

	# Try to add the alias/location to active nodes and active aliases
	def activate_node(self, sender):
		'''Activate a remote node which we either sent to or received from successfully'''
		if sender['location'] == self.location:
			return False

		true_node = self.node_list.matchTo(sender)

		if (true_node not in self.active_nodes and true_node is not None):
			#print('True node:  {0}'.format(true_node))
			self.active_nodes.append(true_node)
			return True
		return False

	def get_node_hash(self):
		'''Create a Node Hash for nodeListHash command'''
		# create a list of publickeys
		publickeys = self.node_list.hash()
		# actually encode
		hashed = hashlib.sha512()
		hashed.update(publickeys.encode('utf-8'))
		return hashed.hexdigest()

	def hash_is_identical(self,hashed):
		'''Wrapper which checks hash equality with remote (could maybe remove)'''
		our_hash = self.get_node_hash()
		return hashed == our_hash

	def get_node_list(self):
		'''Helper method which returns authorized nodes in a standard format'''
		return self.node_list.toJson()

	def authorize(self,sender):
		'''
		Attempt to authorize a node
		'''
		if not self.node_list.isAuthorized(sender):
			self.node_list.add(sender)

	def getPublicKey(self,node):
		matched = self.node_list.matchTo(node)
		public = ""
		if matched is not None:
			public = matched['publicKey']
		return public

	def isActive(self,node):
		if node['location'] == self.location:
			return True

		# Look up the full node details from our authorized nodes
		true_node = self.node_list.matchTo(node)
		return (true_node in self.active_nodes and true_node is not None)

	def isAuthorized(self,node):
		if node['location'] == self.location:
			return True

		# Look up the full node details from our authorized nodes
		true_node = self.node_list.matchTo(node)
		return true_node is not None

	# remove an ip location (location) from active_node_list and its aliases
	def deactivate_node(self, key):
		'''Deactivate a given node'''
		node = self.node_list.matchTo(key)
		if node is not None:
			self.active_nodes.remove(node)
