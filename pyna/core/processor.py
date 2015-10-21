import sys
from pyna.core.relay import Relay
from pyna.base.display import Display
from pyna.core.manager import Manager

class Processor(object):
	'''Controls the behavior of commands that need to be displayed or sent out'''
	def __init__(self, relay, manager):
		self.relay = relay
		self.manager = manager
		self.packager = manager.create_packager()
		self.about()

	def about(self):
		bold_name = Display.bold('PyÑa Colada', Display.color.pyna_colada)
		Display.server_announce('{0} Node v{1}'.format(bold_name, self.manager.version))
		Display.info('A mesh-chat type application written by Evan Kirsch (2015)\n')

	def exit(self):
		Display.server_announce('Closing down node. Thank you for using PyÑa Colada!')
		self.broadcast('disconnection')
		sys.exit(0)

	def whisper(self, message, target):
		whisper_message = self.packager.pack('whisper',message)
		self.relay.send_message(whisper_message,target)

	def reply(self, message):
		self.whisper(message,self.manager.most_recent_whisperer)

	def identity(self,key):
		user = self.manager.getNode(key)
		if user is None:
			Display.info('No user or node was found with key \'{0}\''.format(key))
			return
		self.info(user)

	def importNode(self, filename):
		'''
		Attempt to import a node file
		'''
		new_node = self.manager.importNode(filename)
		if new_node is not None:
			self.full_node_list(new_node)
			return
		Display.warn('Malformed or missing file \'{0}\''.format(filename))

	def info(self,node):
		Display.info("{2}:  {0} ({1})".format(node['alias'],node['uid'],node['location']))

	def who(self):
		if len(self.manager.active_nodes) == 0:
			Display.info('No nodes are active')
			return
		Display.log('Active users')
		for node in self.manager.active_nodes:
			self.info(node)

	def node_list_hash(self,target):
		hashed = self.manager.get_node_hash()
		packed_json = self.packager.pack('nodelisthash',hashed)
		self.relay.send_message(packed_json,target)

	def full_node_list(self,target):
		node_list = self.manager.get_node_list()
		self.send('nodelist',target,node_list)

	def send(self,type,target,content=''):
		packaged_json = self.packager.pack(type,content)
		self.relay.send_message(packaged_json,target)

	def broadcast(self,type,content='',targets=None):
		if targets is None:
			targets = self.manager.active_nodes
		packaged_json = self.packager.pack(type,content)
		self.relay.send_to_all(packaged_json,targets)
