import asyncio
import subprocess
import time
import requests

from api import *


fapi = Func_API()
# fapi.new_token()
# fapi.pc = 'pc0'
# fapi.token = 'qhh53cm5qdz6'
if os.path.exists(config_file):
    fapi.load_config()
else:
    fapi.new_token()
    fapi.save_config()
fapi.fprint()
fapi.online()

async def poling():
    while 1:
        link = f'http://192.168.1.175:9566/pull/{fapi.pc}'
        # print(requests.get(link).json())
        # # print(download_config('l'))
        try:
            l = requests.post(link, data={'token': fapi.token}).json()['token']
            if len(l):
                await fapi.hendler(l)
                
            else:
                await asyncio.sleep(1)

        except:
            print('crashed')
            await asyncio.sleep(1)
        


async def main():
    task1 = asyncio.create_task(poling())

    await task1



asyncio.run(main())

