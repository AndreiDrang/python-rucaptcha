import ssl
import json
import logging
from uuid import uuid4

import websockets
from tenacity import retry, after_log, wait_fixed, stop_after_attempt


class WebSocketRuCaptcha:
    def __init__(self, allSessions: bool = False, suppressSuccess: bool = True):
        """
        Method setup WebSocket connection data
        :param allSessions: `True` if u need send the results of solving captchas to all open sessions.
                            `False` if u will wait captcha result in current session.
        :param suppressSuccess: `False` if u need intermediate info about your task in RuCaptcha system.
                                `True` if u need final answer without any addition info.
        More info - https://wsrucaptcha.docs.apiary.io/#reference/0
        """
        self.sock = None

        self.allSessions = allSessions or False
        self.suppressSuccess = suppressSuccess or True
        # RuCaptcha auth params check
        if not self.allSessions and not self.suppressSuccess:
            raise ValueError(
                f"U set allSessions to `{self.allSessions}` and suppressSuccess to `{self.suppressSuccess}`.\n"
                f"U will not able to get the final result of captcha solving, cause u close the current socket session "
                f"but wait for the result ONLY in the current session(already closed).\n"
                f"Try other param variants:\n"
                f"\tlike default False/True(u will get an answer in this session for this captcha)\n"
                f"\tor True/False(u will get info about the current captcha task and then get captcha solution in all "
                f"opened sessions)"
            )

        self.URL = "wss://s.2captcha.com/"
        # WebSocket SSL setup
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5), after=after_log(logging, logging.ERROR), reraise=True)
    async def socket_session(self):
        """
        Create new socket session
        """
        self.sock = await websockets.connect(self.URL, ssl=self.ssl_context)

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5), after=after_log(logging, logging.ERROR), reraise=True)
    async def socket_session_recreate(self):
        """
        If socket session not exist - create it
        """
        if not self.sock:
            await self.socket_session()

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5), after=after_log(logging, logging.ERROR), reraise=True)
    async def __auth(self) -> dict:
        """
        Method setup connection with RuCaptcha and auth user
        :return: Server response dict
        """
        await self.socket_session_recreate()

        auth_data = {
            "method": "auth",
            "requestId": str(uuid4()),
            "key": self.rucaptcha_key,
            "options": {"allSessions": self.allSessions, "suppressSuccess": self.suppressSuccess},
        }
        await self.sock.send(json.dumps(auth_data))
        return json.loads(await self.sock.recv())

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5), after=after_log(logging, logging.ERROR), reraise=True)
    async def get_request(self) -> dict:
        await self.socket_session_recreate()

        return json.loads(await self.sock.recv())

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5), after=after_log(logging, logging.ERROR), reraise=True)
    async def send_request(self, payload: dict) -> dict:
        """
        Method send request to server and wait response
        :param payload: Dict payload with data
        :return: Server response dict
        """
        await self.socket_session_recreate()

        auth_result = await self.__auth()
        # check if auth is success
        if auth_result["success"]:
            await self.sock.send(json.dumps(payload))
            return await self.get_request()
        else:
            return auth_result
