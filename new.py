import requests

def send_message(text):
    url = f"https://api.telegram.org/bot5707775054:AAGlgA-3myDirI9vyxclNPUqzM4-j1zR6Ts/sendMessage"
    response = requests.post(url, data={'chat_id': -607433374, 'text': text})
    return response.json()['ok']

send_message('dd')