import sys
from core.relay import Relay
from core.display import Display
from core.servermanager import ServerManager
from operator import itemgetter

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
		whisper_to_location = self.manager.get_location(target)
		whisper_message = self.packager.pack('whisper',message)
		print(whisper_to_location)
		self.relay.send_message(whisper_message,whisper_to_location)
		pass

	def connection(self,target):
		connection_message = self.packager.pack('connection')
		self.relay.send_message(connection_message,target)

	def identity(self,key):
		# if this is an alias
		user = self.manager.find_in_active(key)
		if user is None:
			self.display.info('No user or node was found with key \'{0}\''.format(key))
		else:
			self.display('User {0} ({1}) at {2}'.format(user['alias'],user['uid'],user['location']))

	def who(self):
		if len(self.manager.active_nodes) > 0:
			self.display.info('No nodes are active')
			return
		aliases = list(itemgetter('name')(x for x in self.manager.active_nodes))
		print('Active aliases:  {0}\n'.format(aliases))

	def servers(self):
		print('Active servers:  {0}\n'.format(list(self.manager.active_nodes)))

	def chat(self,message):
		self.relay.send_to_all(self.packager.pack('chat',message))

	def serverlisthash(self,target):
		packed_json = self.packager.pack('serverlisthash')
		self.relay.send_message(packed_json,target)

	def ping(self, location):
		ping_json = self.packager.pack('ping')
		self.relay.send_message(ping_json,location)

	# Called by server to see which authorized servers are active
	def ping_all(self):
		ping_json = self.packager.pack('ping')
		for location in self.manager.authorized_nodes:
			self.relay.send_message(ping_json,location)
