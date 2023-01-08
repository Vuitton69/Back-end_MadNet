from flask import Flask
import os
from flask import request, jsonify
from crypter import Crypterast


app = Flask(__name__)

cr = Crypterast()


@app.route('/')
def home():
    return 'You are at home page.'


@app.route('/j!u5xfwd22-w8**8bppt8vm3$86&-50y^hkw1qty')
def l():
    return 'lll'


@app.route("/get", methods=['POST'])  # создание нового ивента
def events_create():
    if request.method == "POST":
        key = request.form['pubkey']
        with open('README.md', 'rb') as f:
            data = f.read()
        t = cr.import_key(key, data)  # .decode('utf8')
        return t


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
