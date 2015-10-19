import json, sys, hashlib
from pynacolada.core.packager import Packager
from pynacolada.base.crypto import Crypto

class Relay(object):
	'''
	Responsible for preparing everything before it is sent. Will include an outbox queue later
	'''
	def __init__(self,sender,display,manager):
		self.sender = sender
		self.display = display
		self.manager = manager

	def send_message(self,message,target):
		'''
		Send a message of any type to a uid/alias/location
		'''
		# Figure out what the location is doing
		node = self.manager.getNode(target)
		if node is None:
			# Erroneous; no user exists here
			self.display.warn('No user was found')
			return

		self.sender.try_to_send(message,node)

		# TODO: Revisit this
		# If not connection or disconnection, warn the user that there's no appropriate user
		#if ('connection' not in message['type'] and target is not None):
		#	# Try to deactivate the node at this target (if it exists)
		#	self.display.warn('mesh-chat application does not appear to exist at {0}'.format(node['location']))
		#	self.manager.deactivate_node(node['location'])

	def send_to_all(self,json,target_nodes):
		'''
		Sends a message to all nodes within the specified target_nodes list
		'''
		for node in target_nodes:
			if node['location'] != self.manager.location:
				self.send_message(json,node)
