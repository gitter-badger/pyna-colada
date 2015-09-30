import sys
from core.relay import Relay
from core.display import Display
from core.servermanager import ServerManager

class Processor(object):
	def __init__(self, relay, display, manager):
		self.relay = relay
		self.display = display
		self.manager = manager
		self.packager = manager.create_packager()

	def about(self):
		self.display.pyna_colada(self.manager.version)
		self.display.info('A mesh-chat type application written by Evan Kirsch (2015)\n')

	def exit(self):
		self.display.server_announce('Closing down server. Thank you for using PyÑa Colada!')
		close_message = self.packager.pack('disconnection')
		self.relay.send_to_all(close_message)
		sys.exit(0)

	def whisper(self, message, target):
		whisper_message = self.packager.pack('whisper',message)
		self.relay.send_message(whisper_message,target)

	def reply(self, message):
		whisper_message = self.packager.pack('whisper',message)
		self.relay.send_message(whisper_message,self.manager.most_recent_whisperer)

	def connection(self,target):
		connection_message = self.packager.pack('connection')
		self.relay.send_message(connection_message,target)

	def identity(self,key):
		# if this is an alias
		user = self.manager.find_in_active(key)
		if user is None:
			self.display.info('No user or node was found with key \'{0}\''.format(key))
		else:
			self.display.info('User {0} ({1}) at {2}'.format(user['alias'],user['uid'],user['address']))

	def who(self):
		if len(self.manager.active_nodes) == 0:
			self.display.info('No nodes are active')
			return
		self.display.log('Active users')
		for node in self.manager.active_nodes:
			self.display.info("{2}:  {0} ({1})".format(node['alias'],node['uid'],node['address']))

	def chat(self,message):
		self.relay.send_to_all(self.packager.pack('chat',message))

	def serverlisthash(self,target):
		hashed = self.manager.get_node_hash()
		packed_json = self.packager.pack('nodeListHash',hashed)
		self.relay.send_message(packed_json,target)

	def full_node_list(self,target):
		node_list = self.manager.get_node_list()
		packed_json = self.packager.pack('nodeListFull',node_list)
		self.relay.send_message(packed_json,target)

	def node_list_diff(self,node_list,target):
		packed_json = self.packager.pack('nodeListDiff',node_list)
		self.relay.send_message(packed_json,target)

	def ping(self, location):
		ping_json = self.packager.pack('ping')
		self.relay.send_message(ping_json,location)

	def pingreply(self, location):
		ping_json = self.packager.pack('pingreply')
		self.relay.send_message(ping_json,location)

	# Called by server to see which authorized servers are active
	def ping_all(self):
		ping_json = self.packager.pack('ping')
		for location in self.manager.authorized_nodes:
			self.relay.send_message(ping_json,location)
