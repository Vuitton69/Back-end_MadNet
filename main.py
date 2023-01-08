from flask import Flask
from flask import request, jsonify
from crypter import Crypterast
from random import choice
from db import DB
import os


app = Flask(__name__)
db = DB()
cr = Crypterast()


@app.route('/')
def home():
    return 'You are at home page.'


@app.route("/get", methods=['POST'])  # создание нового ивента
def gettok():
    if request.method == "POST":
        key = request.form['pubkey']
        db = DB()
        for files in os.listdir('config'):
            try:
                db.write('config_list','name', f"'{files}'")
            except:
                pass
        lst = db.read('config_list WHERE life = 0', 'name')
        print(lst)
        free_token = choice([i[0] for i in lst])
        db.update('config_list', 'life = True', f"name = '{free_token}'")
        with open('config/'+free_token, 'rb') as dt:
            data = dt.read()
        t = cr.import_key(key, data)#.decode('utf8')
        return t


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='0.0.0.0',port=9525)
