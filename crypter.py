from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode


class Crypterast:
    def __init__(self) -> None:
        self.public_key_final = ''

    def generic(self):
        public_key_start_comment = '-----BEGIN PUBLIC KEY-----'
        public_key_end_comment = '-----END PUBLIC KEY-----'

        key = RSA.generate(2048)
        pubkey = key.publickey()

        public_key_pem = pubkey.exportKey(
            format='PEM', passphrase=None, pkcs=1)
        self.public_key_final = str(public_key_pem.decode('ascii')).replace('\n', '').replace(
            public_key_start_comment, '').replace(public_key_end_comment, '').replace(' ', '')

        self._encryptor = PKCS1_OAEP.new(pubkey)
        self._decryptor = PKCS1_OAEP.new(key)

    def import_key(self, key: str, m):
        key = b64decode(key.encode())
        pubKeyObj = RSA.importKey(key)
        decrypto = PKCS1_OAEP.new(pubKeyObj)

        return decrypto.encrypt(m)

    def encrypt(self, text: bytes):
        return self._encryptor.encrypt(text)

    def decrypt(self, text: bytes):
        return self._decryptor.decrypt(text)


if __name__ == '__main__':
    cr = Crypterast()
    cr.generic()
    ba = cr.encrypt(b'encrypt this message')
    baf = cr.decrypt(ba)
    print(ba)
    print(baf)
    cr.import_key(cr.private_key_final, ba)
