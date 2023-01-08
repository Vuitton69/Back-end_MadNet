from random import choice
from db import DB
import os




# print(db.read('links', '*'))
# print(db.delete('links', 'id', '1'))

# print(db.read('links', '*'))


# for i in range(10):
#     t = generate_token()
#     print(t)

class Getter:
    def __init__(self) -> None:
        self.db = DB()
    def read_file(self):
        for files in os.listdir('config'):
            try:
                self.db.write('config_list','name', f"'{files}'")
            except:
                pass
    def get_token(self):
        lst = self.db.read('config_list WHERE life = 0', 'name')
        print(lst)
        free_token = choice([i[0] for i in lst])
        self.db.update('config_list', 'life = True', f"name = '{free_token}'")
        with open('config/'+free_token, 'rb') as dt:
            data = dt.read()
        return data

# gt = Getter()
# print(gt.get_token())
# for i in range(10):
#     with open(f'config/config{i}', 'w') as f:
#         f.write(f'pc{i} {i} [123,321] 0 0')

# conn.commit()
