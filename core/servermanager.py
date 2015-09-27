import json
from core.packager import Packager

class ServerManager(object):
	def __init__(self, alias, address, port):
		self.alias = alias
		self.active_server_list = []
		self.active_aliases = {}
		self.location = '{0}:{1}'.format(address,port)
		self.load()

	def load(self):
		server_config = json.load(open('config/config.json','r'))
		self.version = server_config['version']
		self.uid = server_config['uid']
		self.load_in_servers(self.location)
		self.logger = server_config['logger']
		if self.location == self.logger:
			self.logger = ""

	# Load the servers in out servers.json file into authorized_server_list
	def load_in_servers(self,location):
		self.authorized_server_list = []
		# open the json
		with open('config/servers.json','r') as auth:
			data = json.load(auth)
		# add those which are not already in our authorized_server_list
		for server in data['servers']:
			if (server not in self.authorized_server_list and server != location):
				self.authorized_server_list.append(server)

	def create_packager(self):
		return Packager(self.version,{"name": self.alias, "location": self.location, "uid": self.uid})
