import hashlib, json, os
from core.packager import Packager
from core.nodelist import NodeList

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
		self.uid = config['uid']
		self.node_list.load()

	def createConfig(self):
		data = {"version": "0.4.6","name": "Py\u00d1a Colada","uid": "Anonymous"}
		with open('config/config.json','w') as config:
			json.dump(data, config)

	def importNode(self,filename):
		'''
		Imports a Node so it may connect and initialize into the network
		'''
		return self.node_list.importNode(filename)

	def exportSelf(self):
		'''
		Exports the current settings to a file which can be imported
		'''
		data = {"uid": self.uid, "alias": self.alias, "location": self.location, "publicKey": self.crypto.getPublic().decode('utf-8') }
		with open('{0}.json'.format(self.alias),'w') as auth:
			json.dump(data, auth)

	def create_packager(self):
		'''
		Create a packager from our config settings
		'''
		return Packager(self.version,{"alias": self.alias, "location": self.location, "uid": self.uid})

	def getNode(self, key):
		if type(key) is not dict:
			if key != self.location:
				key = self.find_in_active(key,key,key,key)

		if key['location'] == self.location:
			return None

		return key

	# Try to add the alias/location to active nodes and active aliases
	def activate_node(self, sender):
		'''Activate a remote node which we either sent to or received from successfully'''
		if sender not in self.active_nodes:
			self.active_nodes.append(sender)
			return True
		return False

	def find_in_active(self, alias="", location="", uid="", publicKey=""):
		'''todo rewrite'''
		'''Check to see if any criteria match, and return the respective node if so'''
		for node in self.active_nodes:
			if node['alias'] == alias or node['location'] == location or node['uid'] == uid:
				return node
		return None

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

	# remove an ip location (location) from active_node_list and its aliases
	def deactivate_node(self, key):
		'''Deactivate a given node'''
		node = self.find_in_active(key,key,key,key)
		if node is not None:
			self.active_nodes.remove(node)
