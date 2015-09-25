from datetime import datetime, timezone

class Packager(object):
	def __init__(self,version,alias,location,uid):
		self.version = version
		self.alias = alias
		self.location = location
		self.uid = uid

	def utc_to_local(self,utc_dt):
	    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

	# Package up our data. Most of this will be in a json file, but we're not quite there yet
	def pack(self,message_type,message=""):
		data = {}
		data["type"] = message_type
		data['time_sent'] = self.utc_to_local(datetime.now(timezone.utc)).strftime("%Y-%m-%d %H:%M:%S")
		data["client"] = "Pyna colada"
		data["client_version"] = "v" + self.version
		data["sender"] = {"name": self.alias, "location": self.location, "uid": self.uid}
		data["message"] = message
		return data
