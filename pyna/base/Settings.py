from pyna.base.Crypto import Crypto
from pyna.base.KeyLoader import KeyLoader
from pyna.base.Display import Display
import json, os, pickle, sys, string, random

class Settings(object):
    def __init__(self, alias):
        self.alias = alias
        self.getUid()
        self.createCrypto()

    def getUid(self):
        '''Load UID from users.json or create it'''
        users = json.load(open('config/users.json','r'))
        try:
            self.uid = users[self.alias]
        except Exception as msg:
            self.uid = self.generateUid(32)
            PynaDisplay.warn('Generated New UID: {0}'.format(self.uid))
            users[self.alias] = self.uid
            with open('config/users.json','w') as out:
                json.dump(users, out)

    def generateUid(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))


    def createCrypto(self):
        self.crypto = Crypto()
        self.keyloader = KeyLoader()
        self.loadKeys()

    def generateKeys(self):
        '''
        Generate new RSA-2048 keys for this client (accurate off)
        '''
        Display.log('Generating new keys...')
        self.crypto.generate()
        self.saveKeys()
        Display.log('Done.\n')

    def loadKeys(self):
        '''
        Load public and private key from key.json; generates if empty
        '''
        filename = 'config/.data/{0}.pyna'.format(self.uid)
        if not os.path.isfile(filename):
            self.generateKeys()
            return
        self.passwordLoop(filename)

    def passwordLoop(self, filename):
        '''Loops until the correct password is entered'''
        attempts = 0
        while attempts < 3:
            password = input('Please enter password to unlock ({0} attempts remaining):  '.format(3-attempts))
            try:
                with open(filename,'rb') as enc_data:
                    encrypted = pickle.load(enc_data)
                    data = self.keyloader.unlockWithPassword(password, encrypted)
                    self.crypto.load(data['privateKey'])
                    Display.log('User settings loaded.')
                    return
            except:
                Display.warn('Wrong password')
                attempts += 1

        Display.error('You have exceeded the number of attempts to log in as this user.')
        sys.exit(1)


    def saveKeys(self):
        '''
        Save public and private key to key.json
        '''
        password = input('Please enter password to lock:  ')
        privout = self.crypto.private.exportKey('PEM').decode('utf-8')
        data = json.dumps({"privateKey":privout})
        locked = self.keyloader.lockWithPassword(password, data)
        with open('config/.data/{0}.pyna'.format(self.uid),'wb') as auth:
            pickle.dump(locked, auth)
