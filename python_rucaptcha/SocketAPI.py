import ssl
import json
from uuid import uuid4

import websockets


class WebSocketRuCaptcha:
    def __init__(self):
        self.sock = None
        self.URL = "wss://s.2captcha.com/"
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    async def __auth(self) -> dict:
        auth_data = {
            "method": "auth",
            "requestId": str(uuid4()),
            "key": self.rucaptcha_key,
            "options": {"allSessions": False, "suppressSuccess": False},
        }
        await self.sock.send(json.dumps(auth_data))
        return json.loads(await self.sock.recv())

    async def get_request(self) -> dict:
        return json.loads(await self.sock.recv())

    async def send_request(self, payload: dict) -> dict:
        """
        Method send request to server and wait response
        :param payload: Dict payload with data
        :return: Server response dict
        """
        async with websockets.connect(self.URL, ssl=self.ssl_context) as self.sock:
            auth_result = await self.__auth()
            # check if auth is success
            if auth_result["success"]:
                await self.sock.send(json.dumps(payload))
                return await self.get_request()
            else:
                return auth_result
