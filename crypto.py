from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import hashlib
import zlib
import base64

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

class RSACipher:
    def __init__(self, pair):

        self.pair = pair

        try:
            self.pair['private'] = str.encode(self.pair['private'])
            self.pair['public'] = str.encode(self.pair['public'])
        except:
            pass

        if b'PRIVATE' in pair['private']:
            self.private = RSA.importKey(pair['private'])
        else:
            self.private = None

        self.public = RSA.importKey(pair['public'])

    def encrypt(self, object):
        cipher = PKCS1_OAEP.new(self.public)
        return cipher.encrypt(object)

    def decrypt(self, object):
        cipher = PKCS1_OAEP.new(self.private)
        return cipher.decrypt(object)

    def cube_encrypt(self, object):
        return RSACipher(self.pair).encrypt(str.encode(object)).hex()

class Cube:
    def __init__(self, sequence):

        self.key = hashlib.sha512(str.encode(str(sequence))).hexdigest() # Get a hash of the cube config

        self.rsa_cipher = None
        self.aes_cipher = AESCipher(self.key)
        self.pair = { 'public' : None, 'private' : None }

    def import_pair(self, pair):
        self.pair = pair

        self.pair['public'] = str.encode(self.pair['public'])
        self.pair['private'] = str.encode(self.aes_decrypt(pair['private']))

        self.rsa_cipher = RSACipher(self.pair)

    def export_pair(self):
        public = self.pair['public']
        private = self.aes_encrypt(self.pair['private'])

        export = { 'public' : public, 'private' : private.decode() }

        return export

    def generate_pair(self):
        new_key = RSA.generate(4096, e=65537)
        private_key = new_key.exportKey("PEM")
        public_key = new_key.publickey().exportKey("PEM")

        self.pair = {'public': public_key.decode(), 'private': private_key.decode()}
        self.rsa_cipher = RSACipher(self.pair)

    def aes_encrypt(self, object):
        return self.aes_cipher.encrypt(object)

    def aes_decrypt(self, object):
        return self.aes_cipher.decrypt(object)

    def encrypt(self, object):
        return self.rsa_cipher.encrypt(object).hex()

    def decrypt(self, object):
        return self.rsa_cipher.decrypt(bytes.fromhex(object)).decode()

if __name__ == '__main__':
    c = Cube([123,123,213])
    c.generate_pair()

    lol = c.encrypt(b"Hello, world!")

    thing = c.export_pair()

    #print(c.aes_decrypt(thing['private']))

    m.import_pair(thing)

    print(lol)
    print(m.decrypt(lol))
