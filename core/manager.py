import hashlib, json
from core.packager import Packager

class Manager(object):
	'''Manages all things related to other nodes and configuration settings'''

	def __init__(self, alias, address, port):
		self.alias = alias
		self.active_nodes = []
		self.most_recent_whisperer = None
		self.address = '{0}:{1}'.format(address,port)
		self.load()

	def load(self):
		'''Load all configuration settings and nodes'''
		config = json.load(open('config/config.json','r'))
		self.version = config['version']
		self.uid = config['uid']
		self.load_in_nodes(self.address)
		self.logger = config['logger']
		if self.address == self.logger:
			self.logger = ""

	def load_in_nodes(self,location):
		'''Load in all nodes from our nodes.json file into authorized_nodes'''
		self.authorized_nodes = []
		# open the json
		with open('config/nodes.json','r') as auth:
			data = json.load(auth)
		# add those which are not already in our authorized_node_list
		for node in data['nodes']:
			if (node not in self.authorized_nodes and node != location):
				self.authorized_nodes.append(node)

	def create_packager(self):
		'''Create a packager from our config settings'''
		return Packager(self.version,{"alias": self.alias, "address": self.address, "uid": self.uid, "publicKey": self.alias})

	# not sure if the user typed in a location or alias, so try to get a location
	def get_location(self,key):
		'''Use this to translate an alias, address, or uid into an ip address'''
		# if key is an alias
		node = self.find_in_active(key,key,key,key)
		if node is not None:
			return node['address']
		if type(key) is dict:
			return key['address']
		return key

	# Try to add the alias/location to active nodes and active aliases
	def activate_node(self, sender):
		'''Activate a remote node which we either sent to or received from successfully'''
		if sender not in self.authorized_nodes:
			self.authorize(sender)
		if (sender not in self.active_nodes and sender['address'] != self.address):
			self.active_nodes.append(sender)
			return True
		return False

	def find_in_active(self, alias="", address="", uid="", publickey=""):
		'''Check to see if any criteria match, and return the respective node if so'''
		for node in self.active_nodes:
			if node['alias'] == alias or node['address'] == address or node['uid'] == uid or node['publicKey'] == publickey:
				return node
		return None

	def get_node_hash(self):
		'''Create a Node Hash for nodeListHash command'''
		# create a list of publickeys
		publickeys = ""
		if len(self.authorized_nodes) > 0:
			publickeys = publickeys + self.authorized_nodes[0]['publicKey']
			if len(self.authorized_nodes) > 0:
				for node in self.authorized_nodes[1:]:
					publickeys = publickeys + "{0}".format(node['publicKey'])
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
		return json.dumps({"nodes":self.authorized_nodes})

	def diff_node_list(self,node_list_json):
		'''diff the node list from a json file with our nodes'''
		# Go through and add uniques
		node_list = json.loads(node_list_json)
		self.add_nodes(node_list['nodes'])
		diffed_list = []
		# now finally diff
		for node in self.authorized_nodes:
			if node not in node_list['nodes']:
				diffed_list.append(node)
		return diffed_list

	def add_nodes(self,node_list):
		'''Add a list of nodes to our authorized node list'''
		for node in node_list:
			if node not in self.authorized_nodes:
				self.authorized_nodes.append(node)
		self.save_node_list()

	def authorize(self,sender):
		'''Attempt to authorize a node'''
		if sender in self.authorized_nodes:
			return False
		self.authorized_nodes.append(sender)
		# Update our nodes.json with the new node info
		self.save_node_list()
		return True

	def save_node_list(self):
		'''Save the node list to a file'''
		data = json.load(open('config/nodes.json','r'))
		data.update({"nodes":self.authorized_nodes})
		with open('config/nodes.json','w') as auth:
			json.dump(data, auth)

	# remove an ip address (location) from active_node_list and its aliases
	def deactivate_node(self, key):
		'''Deactivate a given node'''
		node = self.find_in_active(key,key,key,key)
		if node is not None:
			self.active_nodes.remove(node)
