from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
import base64
import hashlib

# Courtesy of https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256/40687785
class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

class Cube:
    def __init__(self, sequence, username):

        self.key = hashlib.sha512(str.encode(str(sequence) + username)).hexdigest() # Get a hash of the cube config

        self.aes_cipher = AESCipher(self.key)
        self.pair = { 'public' : None, 'private' : None }

    def import_pair(self, pair):
        self.pair = pair
        self.pair['private'] = str.encode(self.decrypt(pair['private']))

    def export_pair(self):

        public = self.pair['public']
        private = self.encrypt(self.pair['private'])

        export = { 'public' : public, 'private' : private.decode() }

        return export

    def generate_pair(self):
        new_key = RSA.generate(4096, e=65537)
        private_key = new_key.exportKey("PEM")
        public_key = new_key.publickey().exportKey("PEM")

        self.pair = {'public': public_key, 'private': private_key}

    def encrypt(self, object):
        return self.aes_cipher.encrypt(object.decode())

    def decrypt(self, object):
        return self.aes_cipher.decrypt(object)

import pprint

c = Cube([123,123,213], 'karlzhu')
c.generate_pair()

thing = c.export_pair()

m = Cube([123,123,213], 'karlzhu')

m.import_pair(thing)