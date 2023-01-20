from db import DB

from time import sleep

db = DB()
while 1:
    lst = db.read('config_list', 'name')

    bots = sorted([i[0] for i in lst])
    print(bots)
    sleep(0.05)
db.close()