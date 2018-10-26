import pika
from aiohttp import web

routes = web.RouteTableDef()

"""
Run server:
gunicorn callback_server:main --bind YOUR_HOST_OR_IP:PORT --worker-class aiohttp.GunicornWebWorker --workers 5
"""
# Ответ капчи на сервер приходит ввиде данных с 2 параметрами:
# 'id' - ID задания на рещение капчи 
# 'code' - код решения капчи

def send_data_in_qeue(qeue_key: str, message: dict):
    credentials = pika.PlainCredentials('visitor', 'password')
    parameters = pika.ConnectionParameters('localhost',
                                           5672,
                                           'rucaptcha_vhost',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    json_message = {'id': message.get('id'), 'code': message.get('code')}

    channel.basic_publish(exchange='',
                          routing_key=qeue_key,
                          body=str(json_message))
    print(f" [x] Sent {message}")
    
    connection.close()

@routes.post('/register_key')
async def registr_key(request):
    """
    Регистрация новой очереди в RabbitMQ для получения решний капчи туда
    """
    data = await request.json()
    print(f'New queue created, name - {data};')
    try:
        credentials = pika.PlainCredentials('visitor', 'password')
        parameters = pika.ConnectionParameters('localhost',
                                            5672,
                                            'rucaptcha_vhost',
                                            credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue=data.get("key"))

        connection.close()
        return web.Response(text="OK")

    except Exception as err:
        return web.Response(text="FAIL")

@routes.post('/fun_captcha/{qeue_key}')
async def fun_captcha_handle(request):
    data = await request.post()
    qeue_key = request.match_info['qeue_key']
    send_data_in_qeue(qeue_key=qeue_key, message=data)
    print(f'Fun captcha solution - {data.get("code")}; Captcha ID - {data.get("id")}; Qeue key - {qeue_key};')
    return web.Response(text="fun_captcha")

@routes.post('/image_captcha/{qeue_key}')
async def image_captcha_handle(request):
    data = await request.post()
    qeue_key = request.match_info['qeue_key']
    send_data_in_qeue(qeue_key=qeue_key, message=data)
    print(f'Image captcha solution - {data.get("code")}; Captcha ID - {data.get("id")}; Qeue key - {qeue_key};')
    return web.Response(text="image_captcha")

@routes.post('/key_captcha/{qeue_key}')
async def key_captcha_handle(request):
    data = await request.post()
    qeue_key = request.match_info['qeue_key']
    send_data_in_qeue(qeue_key=qeue_key, message=data)
    print(f'Key captcha solution - {data.get("code")}; Captcha ID - {data.get("id")}; Qeue key - {qeue_key};')
    return web.Response(text="key_captcha")

@routes.post('/media_captcha/{qeue_key}')
async def media_captcha_handle(request):
    data = await request.post()
    qeue_key = request.match_info['qeue_key']
    send_data_in_qeue(qeue_key=qeue_key, message=data)
    print(f'Media captcha solution - {data.get("code")}; Captcha ID - {data.get("id")}; Qeue key - {qeue_key};')
    return web.Response(text="media_captcha")

@routes.post('/recaptcha_captcha/{qeue_key}')
async def recaptcha_captcha_handle(request):
    data = await request.post()
    qeue_key = request.match_info['qeue_key']
    send_data_in_qeue(qeue_key=qeue_key, message=data)
    print(f'ReCaptcha_v2 solution - {data.get("code")}; Captcha ID - {data.get("id")}; Qeue key - {qeue_key};')
    return web.Response(text="recaptcha_captcha")

@routes.post('/rotate_captcha/{qeue_key}')
async def rotate_captcha_handle(request):
    data = await request.post()
    qeue_key = request.match_info['qeue_key']
    send_data_in_qeue(qeue_key=qeue_key, message=data)
    print(f'Rotate captcha solution - {data.get("code")}; Captcha ID - {data.get("id")}; Qeue key - {qeue_key};')
    return web.Response(text="rotate_captcha")

async def main():
    app = web.Application()
    app.add_routes(routes)
    return app
    