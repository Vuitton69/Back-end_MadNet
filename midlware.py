from random import choice
from db import DB


db = DB('bd.db')

# print(db.read('links', '*'))
# print(db.delete('links', 'id', '1'))

# print(db.read('links', '*'))


def generate_token():
    GEN_CONST = [_ for _ in'abcdefghijklmnopqrstuvwxyz0123456789!@$^&*-_=']
    len_no_hash_token = 40
    new_token = ""

    for _ in range(len_no_hash_token):
        new_token += choice(GEN_CONST)
    return new_token

for i in range(10):
    t = generate_token()
    print(t)


# conn.commit()
