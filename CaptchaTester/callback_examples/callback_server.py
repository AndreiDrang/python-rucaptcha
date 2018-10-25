from aiohttp import web

routes = web.RouteTableDef()

"""
Run server:
gunicorn callback_server:main --bind YOUR_HOST_OR_IP:PORT --worker-class aiohttp.GunicornWebWorker --workers 5
"""
# Ответ капчи на сервер приходит ввиде данных с 2 параметрами:
# 'id' - ID задания на рещение капчи 
# 'code' - код решения капчи

@routes.post('/fun_captcha')
async def fun_captcha_handle(request):
    data = await request.post()
    print(f'Fun captcha solution - {data.get("code")}; Captcha ID - {data.get("id")}')
    return web.Response(text="fun_captcha")

@routes.post('/image_captcha')
async def image_captcha_handle(request):
    data = await request.post()
    print(f'Image captcha solution - {data.get("code")}; Captcha ID - {data.get("id")}')
    return web.Response(text="image_captcha")

@routes.post('/key_captcha')
async def key_captcha_handle(request):
    data = await request.post()
    print(f'Key captcha solution - {data.get("code")}; Captcha ID - {data.get("id")}')
    return web.Response(text="key_captcha")

@routes.post('/media_captcha')
async def media_captcha_handle(request):
    data = await request.post()
    print(f'Media captcha solution - {data.get("code")}; Captcha ID - {data.get("id")}')
    return web.Response(text="media_captcha")

@routes.post('/recaptcha_captcha')
async def recaptcha_captcha_handle(request):
    data = await request.post()
    print(f'ReCaptcha_v2 solution - {data.get("code")}; Captcha ID - {data.get("id")}')
    return web.Response(text="recaptcha_captcha")

@routes.post('/rotate_captcha')
async def rotate_captcha_handle(request):
    data = await request.post()
    print(f'Rotate captcha solution - {data.get("code")}; Captcha ID - {data.get("id")}')
    return web.Response(text="rotate_captcha")

async def main():
    app = web.Application()
    app.add_routes(routes)
    return app
    