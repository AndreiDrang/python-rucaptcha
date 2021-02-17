import json
import asyncio
from uuid import uuid4
import base64
import requests
import websockets
import ssl

from serializer import NormalCaptcha

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

API_KEY = "2bfbe92f00f1498e90e1460550b1ad94"
URL = "wss://s.2captcha.com/"


data = {
    "method": "auth",
    "requestId": str(uuid4()),
    "key": API_KEY,
    "options": {"allSessions": True, "suppressSuccess": True},
}
base_64_link = base64.b64encode(
    requests.get("https://pythoncaptcha.tech/static/image/common_image_example/862963.png").content
).decode("utf-8")

normal_captcha = NormalCaptcha(**{
    'method': 'normal',
    'requestId': str(uuid4()),
    'body': base_64_link,
})


async def hello():
    async with websockets.connect(URL, ssl=ssl_context) as sock:
        await sock.send(json.dumps(data))
        res = json.loads(await sock.recv())
        if res['success']:
            print('HOORRRAY')
            print(json.dumps(normal_captcha.dict()))
            print(json.dumps(data))
            await sock.send(json.dumps(normal_captcha.dict()))
            print('Captcha succes send')
            res = json.loads(await sock.recv())

            if res['success']:

                print('Captcha success response - ', res)
            else:
                print('Captcha solving ERRR')
                print(res['error'])
        else:
            print('ERRR')
            print(res['error'])
        print(res['success'])


asyncio.get_event_loop().run_until_complete(hello())
