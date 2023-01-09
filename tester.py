import requests
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


def download_config():
    cr = Crypterast()
    cr.generic()
    pub = cr.public_key_final
    get = 'kerc1syuif&x^9!x*fl9kh@8vw05u4wlsf22ch9r'
    pkey = '8aij&wvq0!1ow^5&x-mdl4sny!gniqxqa-yg*tfy'
    link = 'http://10.0.0.2:9525/'+get
    print(requests.get('http://10.0.0.2:9525/').status_code)
    p = requests.post(link, data={pkey: cr.public_key_final}).content
    with open('configer', 'w') as f:
        f.write(cr.decrypt(p).decode())


download_config()
