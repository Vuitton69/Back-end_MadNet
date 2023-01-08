from random import choice
from db import DB


db= DB('bd.db')

print(db.read('links', '*'))
print(db.delete('links', 'id', '1'))

print(db.read('links', '*'))



def generate_token():
    GEN_CONST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                          'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    len_no_hash_token = 20
    new_token = ""

    

    for _ in range(len_no_hash_token):
        new_token += choice(GEN_CONST)
    return new_token

t = generate_token()
print(t)


# conn.commit()