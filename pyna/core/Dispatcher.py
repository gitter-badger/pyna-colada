import json, sys, hashlib
from pyna.base.Crypto import Crypto
from pyna.core.Packager import Packager
from pyna.ui.PynaDisplay import PynaDisplay

class Dispatcher(object):
	'''
	Responsible for preparing everything before it is sent. Will include an outbox queue later
	'''
	def __init__(self,manager,sender):
		self.sender = sender
		self.manager = manager
		self.packager = manager.getPackager()


	def send(self,type,target,content=''):
		'''
		Send to a single node
		'''
		node = self.manager.getNode(target)
		if node is None:
			# Erroneous; no user exists here
			PynaDisplay.warn('No user was found')
			return

		packaged_json = self.packager.pack(type,content)
		self.sender.try_to_send(packaged_json,node)


	def broadcast(self,type,targets=None,content=''):
		'''
		Send to a set of nodes (default: Active Nodes)
		'''
		if targets is None:
			targets = self.manager.active_nodes

		packaged_json = self.packager.pack(type,content)
		for node in targets:
			if node['location'] != self.manager.location:
				self.sender.try_to_send(packaged_json,node)
