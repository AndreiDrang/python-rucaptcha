import aio_pika
from aiohttp import web

routes = web.RouteTableDef()

"""
Run server:
gunicorn callback_server:main --bind YOUR_HOST_OR_IP:PORT --worker-class aiohttp.GunicornWebWorker --workers 5
"""
# Ответ капчи на сервер приходит ввиде данных с 2 параметрами:
# 'id' - ID задания на рещение капчи 
# 'code' - код решения капчи

async def send_data_in_qeue(qeue_key: str, message: dict):

    connection = await aio_pika.connect_robust("amqp://visitor:password@localhost/rucaptcha_vhost")
        
    channel = await connection.channel()

    json_message = {'id': message.get('id'), 'code': message.get('code')}

    await channel.default_exchange.publish(
            aio_pika.Message(
                body=str(json_message).encode(),
                delivery_mode = 2,
            ),
            routing_key=qeue_key
        )                          
    print(f" [x] Sent {json_message}")
    
    await connection.close()

@routes.post('/register_key')
async def registr_key(request):
    """
    Регистрация новой очереди в RabbitMQ для получения решний капчи туда
    """
    data = await request.json()
    try:
        connection = await aio_pika.connect_robust("amqp://visitor:password@localhost/rucaptcha_vhost")
 
        channel = await connection.channel()

        await channel.declare_queue(data.get("key"), durable=True)
        
        await connection.close()

        print(f'New queue created, name - {data};')
        return web.Response(text="OK")

    except Exception as err:
        print(err)
        return web.Response(text="FAIL")

@routes.post('/rucaptcha/fun_captcha/{qeue_key}')
async def fun_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info['qeue_key']
    await send_data_in_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="fun_captcha")

@routes.post('/rucaptcha/image_captcha/{qeue_key}')
async def image_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info['qeue_key']
    await send_data_in_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="image_captcha")

@routes.post('/rucaptcha/key_captcha/{qeue_key}')
async def key_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info['qeue_key']
    await send_data_in_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="key_captcha")

@routes.post('/rucaptcha/media_captcha/{qeue_key}')
async def media_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info['qeue_key']
    await send_data_in_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="media_captcha")

@routes.post('/rucaptcha/recaptcha_captcha/{qeue_key}')
async def recaptcha_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info['qeue_key']
    await send_data_in_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="recaptcha_captcha")

@routes.post('/rucaptcha/rotate_captcha/{qeue_key}')
async def rotate_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info['qeue_key']
    await send_data_in_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="rotate_captcha")

async def main():
    app = web.Application()
    app.add_routes(routes)
    return app
    