from Crypto.Cipher import AES
from Crypto import Random
from pyna.base.Display import Display
import json, hashlib

def pad(phrase):
    length = 16-(len(phrase) % 16)
    return phrase + bytes([length])*length

def hashPhrase(phrase, type):
    hashed = type()
    hashed.update(phrase)
    return hashed.digest()

def lockWithPassword(password, locked_content):
    hashed = hashPhrase(password.encode('utf-8'), hashlib.sha256)
    aes_iv = hashPhrase(hashed, hashlib.sha1)
    cipher = AES.new(hashed, AES.MODE_CBC, aes_iv[:AES.block_size])

    return cipher.encrypt(pad(locked_content))

def unlockWithPassword(passkey, encrypted):
    passkey = hashPhrase(passkey.encode('utf-8'), hashlib.sha256)
    aes_iv = hashPhrase(passkey, hashlib.sha1)
    aes = AES.new(passkey,AES.MODE_CBC, aes_iv[:AES.block_size])
    
    decrypted = aes.decrypt(encrypted).decode('utf-8')
    end_of_json = decrypted.rfind('}')

    return json.loads(decrypted[:(1+end_of_json)].strip())

while True:
    password = input('Please enter a short password:  ')
    try:
        fully_encrypted = lockWithPassword(password, b'{"message": "contents which are not readable"}')
        break
    except Exception as msg:
        Display.warn('This password is too long. Please try again.  {0}'.format(msg))

while True:
    passkey = input('Please verify your password:  ')
    try:
        data = unlockWithPassword(passkey, fully_encrypted)
        Display.log('Correct password. \nContents are "{0}"\n'.format(data['message']))
        break
    except:
        Display.warn('Incorrect password.\n')
