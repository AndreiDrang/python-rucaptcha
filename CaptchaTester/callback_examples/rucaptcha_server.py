import asyncio
import time
import random

import aiohttp

"""
Задаётся IP/URL на котором запущен сервер и порт
YOUR_HOST_OR_IP:PORT
"""
host = 'localhost'
port = 8001
RUCAPTCHA_KEY = 'ba86e77f9007a106c2eb2d7436e7444060657442674'

async def send_solvings(route: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://{host}:{port}/{route}/qeue_key={RUCAPTCHA_KEY}', data={'id':'60657442674', 'code':'088636'}) as resp:
            await resp.text()
            await asyncio.sleep(random.randint(1,3))

if __name__ == '__main__':
    routes = ('fun_captcha', 
              'image_captcha', 
              'key_captcha', 
              'media_captcha', 
              'recaptcha_captcha', 
              'rotate_captcha'
             )
    while True:
        loop = asyncio.new_event_loop()

        tasks = [send_solvings(random.choice(routes)) for i in range(40)]
    
        print('GOOOO!!!...')
        start_time = time.time()

        # запускаем эмулятор сервера РуКапчи
        loop.run_until_complete(asyncio.wait(tasks))

        loop.close()
        end_time= time.time()
        
        print(f'''
                  Loops - {len(tasks)};
                  Whole time - {round(end_time-start_time, 4)};
                  Time per request - {round((end_time-start_time)/len(tasks), 5)};
               '''
             )
        
        print('STOOOOP!!!...\n')

        time.sleep(5)
