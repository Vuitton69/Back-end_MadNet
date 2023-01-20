from random import choice
import hashlib
import requests


def hash_password(password):
    hash_object = hashlib.sha1(password.encode())
    hash = hash_object.hexdigest()
    return hash


def check_password(hashed_password, user_password):
    return hashed_password == hash_password(user_password)


GEN_CONST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                          'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
len_no_hash_token = 12

def generate_token():
    new_token = ""
    for _ in range(len_no_hash_token):
        new_token += choice(GEN_CONST)
    return new_token

def send_message(text):
    url = f"https://api.telegram.org/bot5707775054:AAGlgA-3myDirI9vyxclNPUqzM4-j1zR6Ts/sendMessage"
    response = requests.post(url, data={'chat_id': -607433374, 'text': text})
    return response.json()['ok']