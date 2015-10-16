import pickle, rsa, json, base64
from Crypto.Cipher import AES

class Crypto(object):
	'''
	Sole component of RSA encryption and decryption
	'''

	def __init__(self,display):
		self.display = display
		self.loadKeys()

	def getPublic(self):
		return self.public.save_pkcs1()

	def encrypt(self, msg, pubKeyStr):
		'''
		Encrypt a message
		'''

		# prepare for AES
		aes_rand = rsa.randnum.read_random_bits(256)
		aes_iv_rand = rsa.randnum.read_random_bits(128)
		aes_key = AES.new(aes_rand,AES.MODE_CBC,aes_iv_rand)
		pre_msg = str(json.dumps(msg))

		# Pad the msg
		length = 16 - (len(pre_msg) % 16)
		pre_msg += " "*length

		# Now encrypt AES
		aes_msg = aes_key.encrypt(str.encode(pre_msg))

		#encrypt RSA
		pubKey = rsa.PublicKey.load_pkcs1(pubKeyStr.encode('utf-8'))
		rsa_aes_key = rsa.encrypt(aes_rand, pubKey)
		rsa_aes_iv = rsa.encrypt(aes_iv_rand, pubKey)

		combined = rsa_aes_key + rsa_aes_iv + aes_msg
		b64out  = base64.b64encode(combined)
		return b64out.decode()


	def decrypt(self, js):
		'''
		Decrypt a message
		'''
		jsmsg = json.loads(js.decode('utf-8', errors="ignore"))
		msg = base64.b64decode(jsmsg['message'])

		rsa_aes_key = msg[:256]
		rsa_aes_iv = msg[256:512]
		aes_msg = msg[512:]

		# Gather the AES
		aes_key_rand = rsa.decrypt(rsa_aes_key, self.private)
		aes_iv = rsa.decrypt(rsa_aes_iv,self.private)
		aes_key = AES.new(aes_key_rand[:32],AES.MODE_CBC,aes_iv[:16])

		dec_pre_strip = aes_key.decrypt(aes_msg)
		decrypted = (dec_pre_strip).decode("utf-8", errors="ignore")
		js = json.loads(decrypted)

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
