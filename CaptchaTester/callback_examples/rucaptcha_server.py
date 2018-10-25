import asyncio
import time
import random

import aiohttp

async def run(route: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://85.255.8.26:80/{route}', data={'id':'60657442674', 'code':'088636'}) as resp:
            await resp.text()
            await asyncio.sleep(random.randint(1,3))

if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    routes = ('fun_captcha', 
              'image_captcha', 
              'key_captcha', 
              'media_captcha', 
              'recaptcha_captcha', 
              'rotate_captcha'
             )

    tasks = [run(random.choice(routes)) for i in range(400)]
    
    print('GOOOO!!!...')

    start_time = time.time()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    end_time= time.time()
    
    print(f'''
            Loops - {len(tasks)};
            Whole time - {round(end_time-start_time, 4)};
            Time per request - {round((end_time-start_time)/len(tasks), 5)};
           ''')
    
    print('STOOOOP!!!...')
