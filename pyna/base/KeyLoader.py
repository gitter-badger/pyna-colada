from Crypto.Cipher import AES
from Crypto import Random
import json, hashlib

class KeyLoader(object):
    '''Used to lock down pyna files with a password'''

    def pad(self, phrase):
        '''Pads a phrase to 16b'''
        remainder = len(phrase) % 16
        if remainder == 0:
            return phrase

        if type(phrase) is str:
            phrase = phrase.encode('utf-8')

        length = 16-remainder
        return phrase + bytes([length])*length

    def hashPhrase(self, phrase, type):
        '''Hash a phrase with a given type (such as hashlib.sha256)'''
        hashed = type()
        hashed.update(phrase)
        return hashed.digest()

    def lockWithPassword(self, password, content_to_lock):
        '''Use a cipher to lock down content with a password'''
        cipher = self.getCipher(password)
        padded = self.pad(content_to_lock)
        return cipher.encrypt(padded)

    def unlockWithPassword(self, password, encrypted):
        '''Use an AES cipher to unlock content with a password'''
        cipher = self.getCipher(password)
        decrypted = cipher.decrypt(encrypted)
        decrypted = decrypted.decode('utf-8')
        end_of_json = decrypted.rfind('}')

        return json.loads(decrypted[:(1+end_of_json)].strip())

    def getCipher(self, password):
        '''Create an AES cipher from a password. Work in Progress'''
        hashed = self.hashPhrase(password.encode('utf-8'), hashlib.sha256)
        aes_iv = self.hashPhrase(hashed, hashlib.sha1)
        return AES.new(hashed, AES.MODE_CBC, aes_iv[:AES.block_size])
