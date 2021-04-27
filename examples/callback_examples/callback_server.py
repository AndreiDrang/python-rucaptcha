import json

import aio_pika
from aiohttp import web
from pymemcache.client import base

routes = web.RouteTableDef()

"""
Run server:
gunicorn callback_server:main --bind YOUR_HOST_OR_IP:PORT --worker-class aiohttp.GunicornWebWorker --workers 5
"""
# Ответ капчи на сервер приходит ввиде данных с 2 параметрами:
# 'id' - ID задания на рещение капчи
# 'code' - код решения капчи

USERNAME = "hard_queue_creator"
PASSWORD = "password"


@routes.post("/register_key")
async def registr_key(request):
    """
    Регистрация новой очереди в RabbitMQ для получения решний капчи туда
    JSON содержит обязательные поля:
    {
        'key': <название очереди>,
        'vhost': <название виртуального хоста: 'rucaptcha_vhost' или 'anticaptcha_vhost'>
    }
    """
    data = await request.json()
    try:
        connection = await aio_pika.connect_robust(f"amqp://{USERNAME}:{PASSWORD}@localhost/{data['vhost']}")

        channel = await connection.channel()

        await channel.declare_queue(data["key"], durable=True)

        await connection.close()

        print(f'New queue created, name - {data["key"]};')
        return web.Response(text="OK")

    except Exception as err:
        print(err)
        return web.Response(text="FAIL")


"""
RuCaptcha service
"""


def save_rucaptcha_result_cache(message: dict):
    # init client
    client = base.Client(("localhost", 11211))
    # set data key-value data to cache
    client.set(message.get("id"), message.get("code"), expire=3600)

    client.close()


async def send_data_in_rucaptcha_qeue(qeue_key: str, message: dict):
    connection = await aio_pika.connect_robust(f"amqp://{USERNAME}:{PASSWORD}@localhost/rucaptcha_vhost")
    channel = await connection.channel()

    json_message = json.dumps({"id": message.get("id"), "code": message.get("code")})

    await channel.default_exchange.publish(
        aio_pika.Message(body=json_message.encode(), delivery_mode=2, expiration=3600),
        routing_key=qeue_key,
    )

    save_rucaptcha_result_cache(message)

    print(f" [x] Sent {json_message}")

    await connection.close()


@routes.get("/ping")
async def status_check(request):
    """
    GET

    Response
    json - {'status': 'OK'}
    """

    # response dict
    data = {"status": "OK"}

    return web.json_response(data)


@routes.get("/rucaptcha/cache/{task_id}")
async def rucaptcha_cache_get_handle(request):
    """
    GET
    task_id - task id from RuCaptcha

    Response
    json - {'id': <task_id>, 'code': <solve_code>}
           or
           {'id': <task_id>, 'code': "CAPCHA_NOT_READY"}
    """
    # get task id from request
    task_id = request.match_info["task_id"]
    # init client
    client = base.Client(("localhost", 11211), connect_timeout=10)
    # get data from key-value cache
    cache_data = client.get(task_id)

    client.close()

    if cache_data:
        # response dict
        data = {"id": task_id, "code": cache_data.decode()}
    else:
        # response dict
        data = {"id": task_id, "code": "CAPCHA_NOT_READY"}

    return web.json_response(data)


@routes.post("/rucaptcha/fun_captcha/{qeue_key}")
async def fun_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info["qeue_key"]
    await send_data_in_rucaptcha_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="fun_captcha")


@routes.post("/rucaptcha/image_captcha/{qeue_key}")
async def image_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info["qeue_key"]
    await send_data_in_rucaptcha_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="image_captcha")


@routes.post("/rucaptcha/key_captcha/{qeue_key}")
async def key_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info["qeue_key"]
    await send_data_in_rucaptcha_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="key_captcha")


@routes.post("/rucaptcha/media_captcha/{qeue_key}")
async def media_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info["qeue_key"]
    await send_data_in_rucaptcha_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="media_captcha")


@routes.post("/rucaptcha/recaptcha_captcha/{qeue_key}")
async def recaptcha_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info["qeue_key"]
    await send_data_in_rucaptcha_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="recaptcha_captcha")


@routes.post("/rucaptcha/rotate_captcha/{qeue_key}")
async def rotate_captcha_handle(request):
    data = await request.post()
    qeue_key_data = request.match_info["qeue_key"]
    await send_data_in_rucaptcha_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="rotate_captcha")


"""
AntiCaptcha service
"""


def save_anticaptcha_result_cache(message: dict):
    # init client
    client = base.Client(("localhost", 11211))
    # set data key-value data to cache
    client.set(message.get("taskId"), json.dumps(message), expire=3600)

    client.close()


async def send_data_in_anticaptcha_qeue(qeue_key: str, message: dict):
    connection = await aio_pika.connect_robust(f"amqp://{USERNAME}:{PASSWORD}@localhost/anticaptcha_vhost")
    channel = await connection.channel()

    json_message = json.dumps({"taskId": message.get("taskId"), "message": message})

    await channel.default_exchange.publish(
        aio_pika.Message(body=json_message.encode(), delivery_mode=2, expiration=3600),
        routing_key=qeue_key,
    )

    save_anticaptcha_result_cache(message)

    print(f" [x] Sent {json_message}")

    await connection.close()


@routes.get("/anticaptcha/cache/{task_id}")
async def anticaptcha_cache_get_handle(request):
    """
    GET
    task_id - task id from AntiCaptcha

    Response
    json - {'taskId': <task_id>, 'message': {<solve_json>}
           or
           {'taskId': <task_id>, 'message': {"taskId": <task_id>, "status": "processing"}
    """
    # get task id from request
    task_id = request.match_info["task_id"]
    # init client
    client = base.Client(("localhost", 11211), connect_timeout=10)
    # get data from key-value cache
    cache_data = client.get(task_id)

    client.close()

    if cache_data:
        # response dict
        data = {"taskId": task_id, "message": json.loads(cache_data.decode())}
    else:
        # response dict
        data = {"taskId": task_id, "message": {"taskId": task_id, "status": "processing"}}

    return web.json_response(data)


@routes.post("/anticaptcha/image_to_text/{qeue_key}")
async def image_to_text_anticaptcha_handle(request):
    data = await request.json()
    qeue_key_data = request.match_info["qeue_key"]

    await send_data_in_anticaptcha_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="image_to_text")


@routes.post("/anticaptcha/nocaptcha/{qeue_key}")
async def nocaptcha_anticaptcha_handle(request):
    data = await request.json()
    qeue_key_data = request.match_info["qeue_key"]

    await send_data_in_anticaptcha_qeue(qeue_key=qeue_key_data, message=data)

    return web.Response(text="nocaptcha")


@routes.post("/anticaptcha/fun_captcha/{qeue_key}")
async def fun_anticaptcha_handle(request):
    data = await request.json()
    qeue_key_data = request.match_info["qeue_key"]

    await send_data_in_anticaptcha_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="fun_captcha")


@routes.post("/anticaptcha/square_net_text_captcha/{qeue_key}")
async def square_net_text_anticaptcha_handle(request):
    data = await request.json()
    qeue_key_data = request.match_info["qeue_key"]

    await send_data_in_anticaptcha_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="square_net_text_captcha")


@routes.post("/anticaptcha/gee_test_captcha/{qeue_key}")
async def gee_test_anticaptcha_handle(request):
    data = await request.json()
    qeue_key_data = request.match_info["qeue_key"]

    await send_data_in_anticaptcha_qeue(qeue_key=qeue_key_data, message=data)
    print(qeue_key_data)

    return web.Response(text="gee_test_captcha")


@routes.post("/anticaptcha/custom_captcha/{qeue_key}")
async def custom_anticaptcha_handle(request):
    data = await request.json()
    qeue_key_data = request.match_info["qeue_key"]

    await send_data_in_anticaptcha_qeue(qeue_key=qeue_key_data, message=data)
    return web.Response(text="custom_captcha")


async def main():
    app = web.Application()
    app.add_routes(routes)
    return app
