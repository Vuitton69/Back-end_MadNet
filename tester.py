import requests
from crypter import Crypterast
cr = Crypterast()
cr.generic()
pub = cr.public_key_final
link = 'http://127.0.0.1:5000/get'
p = requests.post(link, data={'pubkey': cr.public_key_final}).content
p = cr.decrypt(p).decode()
print(p)
