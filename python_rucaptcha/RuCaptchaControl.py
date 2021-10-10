from uuid import uuid4

import aiohttp
import requests

from python_rucaptcha.SocketAPI import WebSocketRuCaptcha

from . import enums
from .base import BaseCaptcha
from .SocketAPI import WebSocketRuCaptcha
from .serializer import ResponseSer, GetRequestSer, CaptchaOptionsSer


class RuCaptchaControl(BaseCaptcha):
    def __init__(self, rucaptcha_key: str, service_type: str = enums.ServicesEnm.TWOCAPTCHA.value, **kwargs):
        """
        Модуль отвечает за дополнительные действия с аккаунтом и капчей.
        :param rucaptcha_key: Ключ от RuCaptcha
        :param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                            и "rucaptcha"
        :param kwargs: Для передачи дополнительных параметров
        """
        # assign args to validator
        self.params = CaptchaOptionsSer(**locals())

        self.get_payload = GetRequestSer(key=self.params.rucaptcha_key, field_json=1).dict(
            by_alias=True, exclude_none=True
        )
        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.get_payload.update({key: kwargs[key]})
        # prepare result payload
        self.result = ResponseSer()

    def additional_methods(self, action: str, **kwargs) -> dict:
        """
        Синхронный метод который выполняет дополнительные действия, такие как жалобы/получение баланса и прочее.
        :param action: Тип действия
        :param kwargs: Для передачи дополнительных параметров
        :return: Возвращает JSON строку с соответствующими полями:
                    serverAnswer - ответ сервера при использовании RuCaptchaControl(баланс/жалобы и т.д.),
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - название ошибки
        Больше подробностей в https://rucaptcha.com/api-rucaptcha#additional
        """
        self.get_payload.update({"action": action})

        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.get_payload.update({key: kwargs[key]})

        try:
            # отправляем на сервер данные с вашим запросом
            answer = requests.get(self.params.url_response, params=self.get_payload)
            if answer.json()["status"] == 0:
                self.result.error = True
                self.result.errorBody = answer.json()["request"]

            elif answer.json()["status"] == 1:
                self.result.serverAnswer = answer.json()["request"]
        except Exception as error:
            self.result.error = True
            self.result.errorBody = error

        finally:
            return self.result.dict(exclude_none=True)


# асинхронный метод
class aioRuCaptchaControl(BaseCaptcha):
    def __init__(self, rucaptcha_key: str, service_type: str = enums.ServicesEnm.TWOCAPTCHA.value, **kwargs):
        """
        Асинхронный модуль отвечает за дополнительные действия с аккаунтом и капчей.
        :param rucaptcha_key: Ключ от RuCaptcha
        :param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        :param kwargs: Для передачи дополнительных параметров
        """
        # assign args to validator
        self.params = CaptchaOptionsSer(**locals())

        self.get_payload = GetRequestSer(key=self.params.rucaptcha_key, field_json=1).dict(
            by_alias=True, exclude_none=True
        )

        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.get_payload.update({key: kwargs[key]})
        # prepare result payload
        self.result = ResponseSer()

    async def additional_methods(self, action: str, **kwargs) -> dict:
        """
        Асинхронный метод который выполняет дополнительные действия, такие как жалобы/получение баланса и прочее.
        :param action: Тип действия
        :param kwargs: Для передачи дополнительных параметров
        :return: Возвращает JSON строку с соответствующими полями:
                    serverAnswer - ответ сервера при использовании RuCaptchaControl(баланс/жалобы и т.д.),
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - название ошибки
        Больше подробностей в https://rucaptcha.com/api-rucaptcha#additional
        """
        self.get_payload.update({"action": action})

        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.get_payload.update({key: kwargs[key]})

        try:
            async with aiohttp.ClientSession() as session:
                # отправляем на сервер данные с вашим запросом
                async with session.get(self.params.url_response, params=self.get_payload) as resp:
                    answer = await resp.json()

            if answer["status"] == 0:
                self.result.error = True
                self.result.errorBody = answer["request"]

            elif answer["status"] == 1:
                self.result.serverAnswer = answer["request"]

        except Exception as error:
            self.result.error = True
            self.result.errorBody = error

        finally:
            return self.result.dict(exclude_none=True)


# Async WebSocket method
class sockRuCaptchaControl(WebSocketRuCaptcha):
    def __init__(self, rucaptcha_key: str, allSessions: bool = None, suppressSuccess: bool = None):
        """
        Method setup WebSocket connection data
        Params description check in parent class
        """
        super().__init__(allSessions, suppressSuccess)
        self.rucaptcha_key = rucaptcha_key

    async def get_balance(self) -> dict:
        """
        The asynchronous WebSocket method return account balance.
        More info - https://wsrucaptcha.docs.apiary.io/#reference/4
        :return: Server response dict
        """
        balance_payload = {
            "method": "balance",
            "requestId": str(uuid4()),
        }
        return await self.send_request(balance_payload)

    async def report(self, success: bool, captchaId: int) -> dict:
        """
        The asynchronous WebSocket method send captcha solving reports (success or fail).
        More info - https://wsrucaptcha.docs.apiary.io/#reference/2
        :param success: Is captcha solved success?
        :param captchaId: Captcha task unique id. For example - 5034284222
        :return: Server response dict
        """
        report_payload = {
            "requestId": str(uuid4()),
            "method": "report",
            "success": success,
            "captchaId": captchaId,
        }

        return await self.send_request(report_payload)
