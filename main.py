from flask import Flask
from flask import request, jsonify
from db import DB
import midlware as md
import new
import bots

app = Flask(__name__)
db = DB()


lst = db.read(f"config_list WHERE name = 'pc0'", 'token')
print(lst)
    
@app.route('/')
def home():
    return 'You are at home page.'


@app.route('/get/<question>')
def find_question(question):
    if question == 'new':

        if bots == []:
            num = 'pc0'
        else:
            num = 'pc' + str(int(bots[-1][2:])+1)

        try:
            token = md.generate_token()
            hash_token = md.hash_password(token)
            db.write('config_list', '`name`,`token`', f"'{num}','{hash_token}'")
            bots.append(num)
            return jsonify({'name': num, 'token': token})

        except:
            return jsonify({'name': False})
            


@app.route("/pull/<pc>", methods=['POST'])
def get_tokdeed(pc):
    if request.method == "POST":
        token = request.form['token']
        lst = db.read(f"events WHERE name = '{pc}'", 'command')
        if md.check_password(lst, token):
            command = request.form['command']
            # with open('new.py','a') as f:
            #     f.write('\na = 3')

        return {'token': False}
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9566, debug=True)
