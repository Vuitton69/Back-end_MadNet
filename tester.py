import requests
from crypter import Crypterast

    
cr = Crypterast()
cr.generic()
pub = cr.public_key_final
link = 'http://127.0.0.1:9525/get'
# p = requests.get(link).content
p = requests.post(link, data={'pubkey': cr.public_key_final}).content
print(p)
with open('configer', 'w') as f:
    f.write(cr.decrypt(p).decode())
    

