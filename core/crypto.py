import pickle, rsa, json
from Crypto.Cipher import AES

class Crypto(object):
	'''
	Sole component of RSA encryption and decryption
	'''

	def __init__(self,display):
		self.display = display
		self.loadKeys()

	def encrypt(self, msg):
		'''
		Encrypt a message
		'''
		# prepare for AES
		aes_rand = rsa.randnum.read_random_bits(256)
		aes_iv_rand = rsa.randnum.read_random_bits(128)
		aes_key = AES.new(aes_rand,AES.MODE_CBC,aes_iv_rand)
		aes_pre_msg = str(json.dumps(msg))

		# Pad the msg
		length = 16 - (len(aes_pre_msg) % 16)
		aes_pre_msg += " "*length

		# Now encrypt AES
		encrypted_aes_msg = aes_key.encrypt(str.encode(aes_pre_msg))

		#encrypt RSA
		rsa_aes_rand = rsa.encrypt(aes_rand, self.public)
		rsa_aes_iv = rsa.encrypt(aes_iv_rand, self.public)

		converted_length = 0
		rsa_aes_msg = b''
		while converted_length < len(encrypted_aes_msg):
			rsa_aes_msg += rsa.encrypt(encrypted_aes_msg[converted_length:(converted_length+245)], self.public)
			converted_length += 245

		return rsa_aes_rand + rsa_aes_iv + rsa_aes_msg

	def decrypt(self, msg):
		'''
		Decrypt a message
		'''
		# Gather the AES
		aes_key_rand = rsa.decrypt(msg[:256], self.private)
		aes_iv = rsa.decrypt(msg[256:512],self.private)

		converted_length = 0
		aes_encrypted = b''
		while converted_length < len(msg[512:]):
			aes_encrypted += rsa.decrypt(msg[(512+converted_length):(768+converted_length)],self.private)
			converted_length += 256

		aes_key = AES.new(aes_key_rand[:32],AES.MODE_CBC,aes_iv[:16])

		dec_pre_strip = aes_key.decrypt(aes_encrypted)
		decrypted = (dec_pre_strip).decode("utf-8", errors="ignore")
		dumpjs = json.dumps(decrypted).strip()
		js = json.loads(dumpjs)
		return js

	def generateKeys(self):
		'''
		Generate new RSA-2048 keys for this client (accurate off)
		'''
		(public,private) = rsa.newkeys(2048,accurate=False)
		self.saveKeys(public,private)
		self.public = public
		self.private = private

	def loadKeys(self):
		'''
		Load public and private key from key.json; generates if empty
		'''
		try:
			with open('config/key.pyna','rb') as key:
				data = pickle.load(key)
				self.public = rsa.PublicKey.load_pkcs1(data['publicKey'])
				self.private = rsa.PrivateKey.load_pkcs1(data['privateKey'])
		except:
			self.display.log('Generating new keys...')
			self.generateKeys()
			self.display.log('Done.\n')

	def saveKeys(self,public,private):
		'''
		Save public and private key to key.json
		'''
		data = {"publicKey":public.save_pkcs1(),"privateKey":private.save_pkcs1()}
		with open('config/key.pyna','wb') as auth:
			pickle.dump(data, auth)
