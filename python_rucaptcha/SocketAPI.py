import ssl
import logging

import websockets
from tenacity import retry, after_log, wait_fixed, stop_after_attempt
from websockets.client import WebSocketClientProtocol

from .base import BaseCaptcha
from .serializer import SockAuthSer, SocketResponse


class WebSocketRuCaptcha(BaseCaptcha):
    def __init__(self, allSessions: bool = False, suppressSuccess: bool = True):
        """
        Method setup WebSocket connection data
        :param allSessions: `True` if u need send the results of solving captchas to all open sessions.
                            `False` if u will wait captcha result in current session.
        :param suppressSuccess: `False` if u need intermediate info about your task in RuCaptcha system.
                                `True` if u need final answer without any addition info.
        More info - https://wsrucaptcha.docs.apiary.io/#reference/0
        """
        self.sock: WebSocketClientProtocol = None
        self.result = SocketResponse()
        self.auth_result = SocketResponse()

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

    async def __socket_session(self):
        """
        Create new socket session
        """
        self.sock = await websockets.connect(self.URL, ssl=self.ssl_context)

    async def __socket_session_recreate(self):
        """
        If socket session not exist - create it
        """
        # if socket not exist
        if not self.sock:
            await self.__socket_session()
        # if socket exist but closed
        elif self.sock.closed:
            await self.sock.close()
            await self.__socket_session()

    async def __auth(self):
        """
        Method setup connection with RuCaptcha and auth user
        :return: Server response dict
        """
        await self.__socket_session_recreate()

        auth_data = SockAuthSer(
            **{
                "key": self.rucaptcha_key,
                "options": {"allSessions": self.allSessions, "suppressSuccess": self.suppressSuccess},
            }
        )
        await self.sock.send(auth_data.json())
        self.auth_result = self.auth_result.parse_raw(await self.sock.recv())

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(3), after=after_log(logging, logging.ERROR), reraise=True)
    async def get_request(self) -> dict:
        await self.__socket_session_recreate()

        response = await self.sock.recv()

        return self.result.parse_raw(response).dict(exclude_none=True)

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(3), after=after_log(logging, logging.ERROR), reraise=True)
    async def send_request(self, payload: str) -> dict:
        """
        Method send request to server and wait response
        :param payload: JSON payload with data
        :return: Server response dict
        """
        await self.__auth()
        # check if auth is success
        if self.auth_result.success:
            await self.sock.send(payload)
            return await self.get_request()
        else:
            return self.auth_result.dict(exclude_none=True)
