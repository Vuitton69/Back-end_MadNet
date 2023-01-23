import requests
from db import DB
import telebot


db = DB()
bot = telebot.TeleBot('5707775054:AAGlgA-3myDirI9vyxclNPUqzM4-j1zR6Ts')


def push_data(text):
    try:
        text = text.split('{')
        name, command = text[0].split()
        args = ','.join([i.split('}')[0] for i in text[1:]])

        data = f'{command},{args}'
        db.write('events', '`name`,`command`', f"'{name.lower()}','{data}'")
        print(data.split(','))
        return 1
    except:
        return 0


@bot.message_handler(content_types=['text'])
def start_message(message):
    print(message.text)
    ans = 'no'

    if push_data(message.text):
        ans = 'Yes'

    bot.send_message(message.chat.id, ans)


bot.infinity_polling()
