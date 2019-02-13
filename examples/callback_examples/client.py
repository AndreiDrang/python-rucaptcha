import asyncio
import json

import aiohttp

from python_rucaptcha import CallbackClient

QUEUE_KEY = 'ba86e77f9007a106c2eb2d7436e7444060657442674'
TASK_ID = '60657442675'

# IP для работы callback`a
HOST = '85.255.8.26'
# PORT для работы callback`a
PORT = 8001
#логин и пароль для подключения к RabbitMQ на callback сервере
RTMQ_USERNAME = 'hardworker_1'
RTMQ_PASSWORD = 'password'
RTMQ_HOST = '85.255.8.26'
RTMQ_PORT = 5672
RTMQ_VHOST = 'rucaptcha_vhost'

async def register_new_queue(route: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://{HOST}:{PORT}/{route}', json={'key':QUEUE_KEY, 'vhost': 'rucaptcha_vhost'}) as resp:
            answer = await resp.text()
            print(f'\tNew queue creation status - {answer};')     


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
        
    # создаём очередь на сервере с ключом
    loop.run_until_complete(register_new_queue(route='register_key'))
    loop.close()    


print(CallbackClient.CallbackClient(task_id=TASK_ID).captcha_handler())

print(CallbackClient.CallbackClient(task_id=TASK_ID, queue_name=QUEUE_KEY, call_type='queue'). \
            captcha_handler(requests_timeout=0.5,
                            auth_params = {
                                            'host': '85.255.8.26',
                                            'port': '8001',
                                            'rtmq_username': 'hardworker_1',
                                            'rtmq_password': 'password',
                                            'rtmq_host': '85.255.8.26',
                                            'rtmq_port': '5672',
                                            'rtmq_vhost': 'rucaptcha_vhost'
                                          }
                            )
     )

