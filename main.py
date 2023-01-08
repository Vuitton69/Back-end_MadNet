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


@app.route("/kerc1syuif&x^9!x*fl9kh@8vw05u4wlsf22ch9r", methods=['POST'])
def get_tok():
    if request.method == "POST":
        key = request.form['8aij&wvq0!1ow^5&x-mdl4sny!gniqxqa-yg*tfy']
        db = DB()
        for files in os.listdir('config'):
            try:
                db.write('config_list', 'name', f"'{files}'")
            except:
                pass
        lst = db.read('config_list WHERE life = 0', 'name')
        print(lst)
        free_token = choice([i[0] for i in lst])
        db.update('config_list', 'life = True', f"name = '{free_token}'")
        with open('config/'+free_token, 'rb') as dt:
            data = dt.read()
        t = cr.import_key(key, data)
        return t


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9525)
