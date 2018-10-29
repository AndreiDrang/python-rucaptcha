import asyncio
import time
import random

import pika
import aiohttp

"""
Задаётся IP/URL на котором запущен сервер и порт
YOUR_HOST_OR_IP:PORT
"""
host = '85.255.8.26'
port = 80
RUCAPTCHA_KEY = 'ba86e77f9007a106c2eb2d7436e7444060657442674'

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    channel.basic_ack(delivery_tag = method.delivery_tag)
    channel.stop_consuming()
def wait_queue_elements(queue_name: str):

    credentials = pika.PlainCredentials('visitor', 'password')
    parameters = pika.ConnectionParameters(host,
                                           5672,
                                           'rucaptcha_vhost',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.basic_consume(callback, queue=queue_name, arguments={'captcha_id': 6666})

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


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
        
    print('STOOOOP!!!...')

    wait_queue_elements(RUCAPTCHA_KEY)
