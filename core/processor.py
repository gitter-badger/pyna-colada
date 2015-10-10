import sys
from core.relay import Relay
from core.display import Display
from core.manager import Manager

class Processor(object):
	'''Controls the behavior of commands that need to be displayed or sent out'''
	def __init__(self, relay, display, manager):
		self.relay = relay
		self.display = display
		self.manager = manager
		self.packager = manager.create_packager()

	def about(self):
		self.display.pyna_colada(self.manager.version)
		self.display.info('A mesh-chat type application written by Evan Kirsch (2015)\n')

	def exit(self):
		self.display.server_announce('Closing down node. Thank you for using PyÑa Colada!')
		self.broadcast('disconnection')
		sys.exit(0)

	def whisper(self, message, target):
		whisper_message = self.packager.pack('whisper',message)
		self.relay.send_message(whisper_message,target)

	def reply(self, message):
		self.whisper(message,self.manager.most_recent_whisperer)

	def identity(self,key):
		# if this is an alias
		user = self.manager.find_in_active(key)
		if user is None:
			self.display.info('No user or node was found with key \'{0}\''.format(key))
		else:
			self.info(user)

	def help(self):
		self.display.info('/w <Target> sends a whisper private message to an location, alias, or uid')
		self.display.info('/r sends a whisper to the most recent whisperer')
		self.display.info('/who displays information about all active nodes')
		self.display.info('/con <Target> connects to a target')
		self.display.info('/ping <Target> pings a target')
		self.display.info('/pingall pings all authorized nodes')
		self.display.info('/exit closes this node\n')

	def who(self):
		if len(self.manager.active_nodes) == 0:
			self.display.info('No nodes are active')
			return
		self.display.log('Active users')
		for node in self.manager.active_nodes:
			self.info(node)

	def info(self,node):
		self.display.info("{2}:  {0} ({1})".format(node['alias'],node['uid'],node['location']))

	def node_list_hash(self,target):
		hashed = self.manager.get_node_hash()
		packed_json = self.packager.pack('nodelisthash',hashed)
		self.relay.send_message(packed_json,target)

	def full_node_list(self,target):
		node_list = self.manager.get_node_list()
		self.send('nodelistfull',target,node_list)

	def node_list_diff(self,node_list,target):
		self.send('nodelistdiff',target,node_list)

	def send(self,type,target,content=''):
		packaged_json = self.packager.pack(type,content)
		self.relay.send_message(packaged_json,target)

	def broadcast(self,type,content='',targets=None):
		if targets is None:
			targets = self.manager.active_nodes
		packaged_json = self.packager.pack(type,content)
		self.relay.send_to_all(packaged_json,targets)
