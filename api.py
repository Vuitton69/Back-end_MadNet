import requests


class Func_API:
    def __init__(self, pc, token) -> None:
        self.pc = pc
        self.token = token
        self.id_op = 0
        self.istd = ''
        self.ostd = ''
        self.url = 'http//95.181.224.52:9566'

    def new_token(self):
        url = self.url + '/get/new'
        response = requests.post(url).json()
        if response['name']:
            self.pc = response['name']
            self.token = response['token']
            return True
        else:
            return False

    def send_answer(self):
        data = {'token': self.token,
                'id': self.id_op,
                'answer': self.ostd
                }
        requests.post(self.url + f"/push/{self.pc}", data=data)
