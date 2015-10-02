import json, sys, hashlib
from core.packager import Packager

class Relay(object):
	'''Responsible for preparing everything before it is sent. Will include an outbox queue later'''

	def __init__(self,sender,display,servermanager):
		self.sender = sender
		self.display = display
		self.manager = servermanager


	def send_message(self,message,target):
		'''Send a message of any type to a uid/alias/address'''
		# Figure out what the address is doing
		address = self.manager.get_location(target)
		if address is None:
			# Erroneous; no user exists here
			self.display.warn('No user was found at {0}'.format(target))
			return
		# Try to send the message
		if self.sender.try_to_send(message,address):
			# everything went according to plan so just exit
			return
		# If not connection or disconnection, warn the user that there's no appropriate user
		if ('connection' not in message['type'] and target is not None):
			self.display.warn('mesh-chat application does not appear to exist at {0}'.format(address))
			# Try to deactivate the node at this target (if it exists)
			self.manager.deactivate_node(address)


	def send_to_all(self,json,target_nodes):
		'''Sends a message to all nodes within the specified target_nodes list'''
		for node in target_nodes:
			address = self.manager.get_location(node['address'])
			if address != self.manager.address:
				self.send_message(json,address)
