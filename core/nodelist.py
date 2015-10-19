import json

class NodeList(object):

	def load(self):
		'''
		Load in all nodes from our nodes.json file into authorized_nodes
		'''
		self.authorized_nodes = []
		# open the json
		with open('config/nodes.json','r') as auth:
			data = json.load(auth)
			self.authorized_nodes = data['nodes']

	def save(self):
		'''
		Save the node list to a file
		'''
		data = json.load(open('config/nodes.json','r'))
		data.update({"nodes":self.authorized_nodes})
		with open('config/nodes.json','w') as auth:
			json.dump(data, auth)

	def addList(self,node_list):
		'''
		Add a list of nodes to our authorized node list
		'''
		for node in [x for x in node_list if x not in self.authorized_nodes]:
			self.authorized_nodes.append(node)
		self.save()

	def add(self,node):
		'''
		Add a list of nodes to our authorized node list
		'''
		if node not in self.authorized_nodes:
			self.authorized_nodes.append(node)
			self.save()

	def importNode(self,filename):
		'''
		Imports a Node so it may connect and initialize into the network
		'''
		new_node = None
		try:
			new_node = json.load(open(filename,'r'))
			self.authorized_nodes.append(new_node)
			self.save()
		except Exception as msg:
			print(msg)
		return new_node

	def hash(self):
		'''
		Returns a nodelist hash
		'''
		return ",".join([x['publicKey'] for x in self.authorized_nodes])

	def toJson(self):
		'''
		Straightforward; dumps to JSON
		'''
		return self.authorized_nodes

	def matchTo(self, criterion):
		'''
		Looks up an active node and gets its respective public key
		'''
		return_node = [node for node in self.authorized_nodes for key in criterion.keys() if criterion[key] == node[key]]
		if len(return_node) > 0:
			return return_node[0]
		return None

	def exists(self,criterion):
		'''
		Checks to see if an authorized node meets a given criterion
		'''
		vals = [node.values() for node in self.authorized_nodes]
		return criterion in [y for v in vals for y in v]

	def diff(self,node_list):
		'''
		add uniques to our list, then return a list unique to sender
		'''
		self.addList(node_list)
		return [node for node in self.authorized_nodes if node not in node_list]

	def isAuthorized(self,node):
		'''
		Check to see if a node is authorized
		'''
		return [node in self.authorized_nodes]
