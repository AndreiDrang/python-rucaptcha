import asyncio
import time
import random
import json

import pika
import aiohttp

"""
Задаётся IP/URL на котором запущен сервер и порт
YOUR_HOST_OR_IP:PORT
"""
host = '85.255.8.26'
port = 8001
RUCAPTCHA_KEY = 'ba86e77f9007a106c2eb2d7436e7444060657442674'
TASK_ID = '60657442675'

USERNAME = 'hardworker_1'
PASSWORD = 'password'

def wait_message(queue_name: str, task_id: str, channel: pika.adapters.blocking_connection.BlockingChannel):
    print('Ожидание решения капчи в очереди')
    while True:
        method_frame, header_frame, body = channel.basic_get(queue_name)
        if body:
            json_body = json.loads(body.decode())
            
            if json_body.get('id')==task_id:
                channel.basic_ack(method_frame.delivery_tag)
                return json_body
            else:
                continue
        else:
            continue
        # ставим небольшую задержку что бы не спамить сервер rabbitmq
        time.sleep(0.5)

def wait_answer_from_qeue(queue_name: str, task_id: str):
    parameters = pika.URLParameters(f'amqp://{USERNAME}:password@{host}:5672/rucaptcha_vhost')
    connection = pika.BlockingConnection(parameters=parameters)

    channel = connection.channel()
    answer = wait_message(queue_name=queue_name, task_id=task_id, channel=channel)

    print(answer.get('id'))

async def register_new_qeue(route: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://{host}:{port}/{route}', json={'key':RUCAPTCHA_KEY}) as resp:
            answer = await resp.text()
            print(f'\tNew queue creation status - {answer};')     

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    
    print('GOOOO!!!...')
    # создаём очередь на сервере с ключом
    loop.run_until_complete(register_new_qeue(route='register_key'))
    loop.close()    
    print('STOOOOP!!!...')

    #wait_queue_elements(RUCAPTCHA_KEY)
    # ожидание конкретного сообщения от сервера
    wait_answer_from_qeue(RUCAPTCHA_KEY, TASK_ID)
