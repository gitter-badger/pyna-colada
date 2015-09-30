import json
from core.packager import Packager

class ServerManager(object):
	def __init__(self, alias, address, port):
		self.alias = alias
		self.active_nodes = []
		self.address = '{0}:{1}'.format(address,port)
		self.load()

	def load(self):
		server_config = json.load(open('config/config.json','r'))
		self.version = server_config['version']
		self.uid = server_config['uid']
		self.load_in_servers(self.address)
		self.logger = server_config['logger']
		if self.address == self.logger:
			self.logger = ""

	# Load the servers in out servers.json file into authorized_server_list
	def load_in_servers(self,location):
		self.authorized_nodes = []
		# open the json
		with open('config/nodes.json','r') as auth:
			data = json.load(auth)
		# add those which are not already in our authorized_server_list
		for server in data['nodes']:
			if (server not in self.authorized_nodes and server != location):
				self.authorized_nodes.append(server)

	def create_packager(self):
		return Packager(self.version,{"alias": self.alias, "address": self.address, "uid": self.uid, "publicKey": self.alias})

	# not sure if the user typed in a location or alias, so try to get a location
	def get_location(self,key):
		# if key is an alias
		node = self.find_in_active(key,key,key,key)
		if node is not None:
			return node['address']
		if type(key) is dict:
			return key['address']
		return key

	# Try to add the alias/location to active servers and active aliases
	def activate_node(self, sender):
		if sender not in self.active_nodes:
			self.active_nodes.append(sender)
			return True
		return False

	def find_in_active(self, alias="", address="", uid="", publickey=""):
		for node in self.active_nodes:
			if node['alias'] == alias or node['address'] == address or node['uid'] == uid or node['publicKey'] == publickey:
				return node
		return None

	def authorize(self,sender):
		if sender in self.authorized_nodes:
			return False
		self.authorized_nodes.append(sender)
		# Update our servers.json with the new server info
		data = json.load(open('config/nodes.json','r'))
		data.update({"nodes":self.authorized_nodes})
		with open('config/nodes.json','w') as auth:
			json.dump(data, auth)
		return True

	# remove an ip address (location) from active_server_list and its aliases
	def deactivate_node(self, key):
		node = self.find_in_active(key,key,key,key)
		if node is not None:
			self.active_nodes.remove(node)
