from db import DB
from time import sleep

db = DB()
for i in range(3,100):
    db.write('config_list', '`name`,`token`', f"'pc{i}','hash_token'")

    sleep(0.5)
db.close()