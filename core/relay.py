import json, sys, hashlib
from core.packager import Packager

class Relay(object):
	def __init__(self,sender,display,servermanager):
		self.sender = sender
		self.display = display
		self.manager = servermanager

	def send_message(self,message,target):
		address = self.manager.get_location(target)
		if address is None:
			self.display.warn('No user was found at {0}'.format(target))
			return
		if self.sender.try_to_send(message,address):
			return
		if (message['type'] != 'connection' and target is not None):
			self.display.warn('mesh-chat application does not appear to exist at {0}'.format(address))
			self.manager.deactivate_node(address)

	# Send JSON to all active servers
	def send_to_all(self,json):
		for active_server in self.manager.active_nodes:
			address = self.manager.get_location(active_server['address'])
			self.send_message(json,address)
