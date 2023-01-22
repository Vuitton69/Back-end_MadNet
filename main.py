from flask import Flask
from flask import request, jsonify
from db import DB
import midlware as md

app = Flask(__name__)
db = DB()

bot = db.read('config_list', 'name')
bots = sorted([i[0] for i in bot])


@app.route('/')
def home():
    return 'You are at home page.'


@app.route('/get/<question>', methods=['POST'])
def find_question(question):
    if question == 'new':

        if bots == []:
            num = 'pc0'
        else:
            num = 'pc' + str(int(bots[-1][2:])+1)

        try:
            token = md.generate_token()
            hash_token = md.hash_password(token)
            db.write('config_list', '`name`,`token`',
                     f"'{num}','{hash_token}'")
            bots.append(num)
            return jsonify({'name': num, 'token': token})

        except:
            return jsonify({'name': False})


@app.route("/pull/<pc>", methods=['POST'])
def get_token(pc):
    if request.method == "POST":
        token = request.form['token']
        htoken = db.read(f"config_list WHERE name = '{pc}'", 'token')[0][0]

        if md.check_password(htoken, token):
            com = db.read(
                f"events WHERE name = '{pc}' ", 'id, command')

            com = sorted([list(i) for i in com])
            print(com)
            return {'token': com}

        return {'token': False}


@app.route("/push/<pc>", methods=['POST'])
def push_text(pc):
    if request.method == "POST":
        try:
            token = request.form['token']
            htoken = db.read(f"config_list WHERE name = '{pc}'", 'token')[0][0]

            if md.check_password(htoken, token):
                id = request.form['id']
                answer = request.form['answer'] 
                answer = f'{pc}\n{answer}'
                md.send_message(answer)
                db.delete('events', 'id' f"'{id}'")

                return {'token': True}
        except:
            return {'token': False}

@app.route("/online/<pc>", methods=['POST'])
def online(pc):
    if request.method == "POST":

        token = request.form['token']
        htoken = db.read(f"config_list WHERE name = '{pc}'", 'token')[0][0]

        if md.check_password(htoken, token):
            answer = request.form['answer'] 
            md.send_message(answer)

            return {'token': True}
        # except:
        return {'token': False}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9566, debug=True)
