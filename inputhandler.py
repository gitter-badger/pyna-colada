import json, sys
from packager import Packager

class InputHandler(object):
	def __init__(self,sender,display,servermanager):
		self.sender = sender
		self.display = display
		self.configuration = servermanager
		self.packager = servermanager.create_packager()

	# determines what to do with the string from wait_for_input
	def process(self,message):
		if message is "":
			return

		# User wants to connect to a specific ip:port pair
		if '/con ' in message[:5]:
			connection_message = self.packager.pack('connection')
			self.send_message(connection_message,message[3:])
			return
		# User wants to whisper to an alias (if it exists)
		if '/w ' in message[:3]:
			if len(message) is 3:
				self.display.warn('Cannot send a whisper without a target or message.')
				return
			try:
				index_of_space = 3 + message[3:].index(' ')
			except:
				self.display.warn('Cannot send a whisper without a message.')
				return
			whisper_to_location = self.get_location(message[3:index_of_space])
			whisper_message = self.packager.pack('whisper',message[index_of_space+1:])
			self.send_message(whisper_message,whisper_to_location)
			return
		# User wants to reply to the most recent whisperer (if it exists)
		if '/r ' in message[:3]:
			whisper_message = self.packager.pack('whisper',message[3:])
			whisper_to_location = self.configuration.active_aliases[self.configuration.most_recent_whisperer]
			self.send_message(whisper_message,whisper_to_location)
			return
		# User wants to disconnect this node
		if '/exit' in message[:5]:
			self.display.server_announce('Closing down server. Thank you for using PyÑa Colada!')
			close_message = self.packager.pack('disconnection')
			self.send_to_all(close_message)
			sys.exit(0)
			return
		# User wants to ping its active serverlist
		if '/pingall' in message[:8]:
			self.ping_all()
			return
		# User wants a ping update from only a specific node
		if '/ping ' in message[:6]:
			packed_json = self.packager.pack('ping')
			location = self.get_location(message[6:])
			self.send_message(packed_json,location)
			return
		# User wants to know more information about an alias or ipaddress
		if '/? ' in message[:3]:
			key = message[3:]
			# if this is an alias
			if key in self.configuration.active_aliases:
				self.display.info('User \'{0}\' at location {1}'.format(key,self.configuration.active_aliases[key]))
				return
			# if this is an ipaddress
			if key in self.configuration.active_server_list:
				# look for the corresponding alias for this address. Not pretty but it works
				if key in self.configuration.active_aliases.values():
					for alias in self.configuration.active_aliases.items():
						if alias[1] == key:
							self.display.info('User \'{0}\' at location {1}'.format(alias[0],key))
							return
				# in case there is no known user alias
				self.display.info('Unknown user at location {0}'.format(key))
				return
			# found nothing
			self.display.info('No user or node was found with key \'{0}\''.format(key))
		# User wants to know what servers are active
		if '/servers' in message[:8]:
			print('Active servers:  {0}\n'.format(list(self.configuration.active_server_list)))
			return
		# User wants to know which aliases are active
		if '/who' in message[:4]:
			print('Active aliases:  {0}\n'.format(list(self.configuration.active_aliases.keys())))
			return
		# User wants to know more about the application
		if '/about' in message[:6]:
			self.display.pyna_colada(self.configuration.version)
			self.display.info('A mesh-chat type application written by Evan Kirsch (2015)\n')
			return

		# default: send a chat message
		packed_json = self.packager.pack('chat',message)
		self.send_to_all(packed_json)

	def send_text_message(self,message,target):
		self.send_message(self.packager.pack('chat',message),target)

	def send_message(self,message,target):
		if self.sender.try_to_send(target, message):
			self.activate_server(target)
		elif message['type'] != 'connection':
			self.display.warn('mesh-chat application does not appear to exist at {0}'.format(target))
			self.deactivate_server(target)

	# Called by server to see which authorized servers are active
	def ping_all(self):
		ping_json = self.packager.pack('ping')
		for address in self.configuration.authorized_server_list:
			self.sender.try_to_send(address,ping_json)

	# not sure if the user typed in a location or alias, so try to get a location
	def get_location(self,key):
		# if key is an alias
		if key in self.configuration.active_aliases:
			return self.configuration.active_aliases[key]

		# if key is a location
		if key in self.configuration.active_server_list:
			return key

	# Send a Connection message to a location
	def send_type_to_location(self,message_type,target):
		message = self.packager.pack(message_type)
		self.send_message(message,target)

	# Send JSON to all active servers
	def send_to_all(self,json):
		for active_server in self.configuration.active_server_list:
			self.send_message(json,active_server)

	# Try to add the alias/location to active servers and active aliases
	def activate_server(self, location, alias=""):
		if location not in self.configuration.active_server_list:
			self.configuration.active_server_list.append(location)
			self.send_type_to_location('serverlisthash',location)
		if alias is not "" and alias not in self.configuration.active_aliases:
			self.configuration.active_aliases[alias] = location
			self.display.log('Registered {0} at {1}'.format(alias,location))

	# remove an ip address (location) from active_server_list and its aliases
	def deactivate_server(self, location):
		if location in self.configuration.active_server_list:
			self.configuration.active_server_list.remove(location)
		if location in list(self.configuration.active_aliases.values()):
			self.configuration.active_aliases = {k:v for k,v in self.configuration.active_aliases.items() if v != location}
