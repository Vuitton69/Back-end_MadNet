from db import DB

db = DB()

lst = db.read('config_list', 'name')
bots = sorted([i[0] for i in lst])

db.close()