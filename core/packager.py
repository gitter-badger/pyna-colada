from datetime import datetime, timezone

class Packager(object):
	'''Factory class responsible for packaging outgoing json in an appropriate format'''

	def __init__(self,version,sender_details):
		self.version = version
		self.senderdetails = sender_details

	def utc_to_local(self,utc_dt):
		'''Changes the UTC timezone to local timezone'''
	    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

	# Package up our data. Most of this will be in a json file, but we're not quite there yet
	def pack(self,message_type,message=""):
		'''Main factory method; produces appropriately formatted json'''
		data = {}
		data["type"] = message_type
		data['time_sent'] = self.utc_to_local(datetime.now(timezone.utc)).strftime("%Y-%m-%d %H:%M:%S")
		data["client"] = "Pyna colada"
		data["client_version"] = "v" + self.version
		data["sender"] = self.senderdetails
		data["message"] = message
		return data
