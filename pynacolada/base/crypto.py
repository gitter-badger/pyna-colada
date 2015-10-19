import pickle, json, base64
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto import Random

class Crypto(object):
	'''
	Sole component of RSA encryption and decryption
	'''

	def __init__(self,display):
		self.display = display
		self.loadKeys()

	def getPublic(self):
		return self.private.publickey().exportKey('PEM')

	def encrypt(self, msg, pubKeyStr):
		'''
		Encrypt a message
		'''
		# prepare for AES
		aes_rand = Random.new().read(32)
		aes_iv_rand = Random.new().read(AES.block_size)
		aes_key = AES.new(aes_rand,AES.MODE_CBC,aes_iv_rand)
		pre_msg = str(json.dumps(msg))

		# Pad the msg
		length = 16 - (len(pre_msg) % 16)
		pre_msg += " "*length

		# Now encrypt AES
		aes_msg = aes_key.encrypt(str.encode(pre_msg))

		# Prepare PKCS1 1.5 Cipher
		pubKey = RSA.importKey(pubKeyStr)
		cipher = PKCS1_v1_5.new(pubKey)

		# encrypt RSA
		rsa_aes_key = cipher.encrypt(aes_rand)
		rsa_aes_iv = cipher.encrypt(aes_iv_rand)

		combined = rsa_aes_key + rsa_aes_iv + aes_msg
		b64out  = base64.b64encode(combined)
		return b64out.decode()


	def decrypt(self, js):
		'''
		Decrypt a message
		'''
		jsdec = js.decode('utf-8', errors="ignore")
		jsmsg = json.loads(jsdec.strip())
		msg = base64.b64decode(jsmsg['message'])

		rsa_aes_key = msg[:256]
		rsa_aes_iv = msg[256:512]
		aes_msg = msg[512:]

		# Gather the AES
		aes_key_rand = self.cipher.decrypt(rsa_aes_key,None)
		aes_iv = self.cipher.decrypt(rsa_aes_iv,None)
		aes_key = AES.new(aes_key_rand[:32],AES.MODE_CBC,aes_iv[:AES.block_size])

		# strip out padding at the end and load as json
		dec_pre_strip = aes_key.decrypt(aes_msg)
		decrypted = (dec_pre_strip).decode("utf-8", errors="ignore")
		end_of_json = decrypted.rfind('}')
		js = json.loads(decrypted[:(1+end_of_json)].strip())

		return js

	def generateKeys(self):
		'''
		Generate new RSA-2048 keys for this client (accurate off)
		'''
		self.private = RSA.generate(2048)
		#(public,private) = rsa.newkeys(2048,accurate=False)
		self.saveKeys()

	def loadKeys(self):
		'''
		Load public and private key from key.json; generates if empty
		'''
		try:
			with open('config/key.pyna','rb') as key:
				data = pickle.load(key)
				self.private = RSA.importKey(data['privateKey'])
		except:
			self.display.log('Generating new keys...')
			self.generateKeys()
			self.display.log('Done.\n')

		self.cipher = PKCS1_v1_5.new(self.private)

	def saveKeys(self):
		'''
		Save public and private key to key.json
		'''
		privout = self.private.exportKey('PEM').decode('utf-8')
		data = {"privateKey":privout}

		with open('config/key.pyna','wb') as auth:
			pickle.dump(data, auth)
