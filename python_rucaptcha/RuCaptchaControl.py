from uuid import uuid4

import aiohttp
import requests

from python_rucaptcha.SocketAPI import WebSocketRuCaptcha
from python_rucaptcha.decorators import api_key_check, service_check


class RuCaptchaControl:
    def __init__(self, rucaptcha_key: str, service_type: str = "2captcha", **kwargs):
        """
        Модуль отвечает за дополнительные действия с аккаунтом и капчей.
        :param rucaptcha_key: Ключ от RuCaptcha
        :param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                            и "rucaptcha"
        """
        self.service_type = service_type
        self.post_payload = {"key": rucaptcha_key, "json": 1}
        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    @api_key_check
    @service_check
    def additional_methods(self, action: str, **kwargs):
        """
        Метод который выполняет дополнительные действия, такие как жалобы/получение баланса и прочее.
        :param action: Тип действия, самые типичные:
                            getbalance(получение баланса),
                            reportbad(жалоба на неверное решение).
                            reportgood(оповещение при верном решении капчи, для сбора статистики по ReCaptcha V3)
        :param kwargs: Для передачи дополнительных параметров
        :return: Возвращает JSON строку с соответствующими полями:
                    serverAnswer - ответ сервера при использовании RuCaptchaControl(баланс/жалобы и т.д.),
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - название ошибки
        Больше подробностей и примеров можно прочитать в 'CaptchaTester/rucaptcha_control_example.py'
        """
        # result, url_response - задаются в декораторе `service_check`, после проверки переданного названия

        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        self.post_payload.update({"action": action})

        try:
            # отправляем на сервер данные с вашим запросом
            answer = requests.post(self.url_response, data=self.post_payload)
        except Exception as error:
            self.result.update({"error": True, "errorBody": {"text": error, "id": -1}})
            return self.result

        if answer.json()["status"] == 0:
            self.result.update({"error": True, "errorBody": answer.json()["request"]})
            return self.result

        elif answer.json()["status"] == 1:
            self.result.update({"serverAnswer": answer.json()["request"]})
            return self.result


# асинхронный метод
class aioRuCaptchaControl:
    def __init__(self, rucaptcha_key: str, service_type: str = "2captcha", **kwargs):
        """
        Асинхронный модуль отвечает за дополнительные действия с аккаунтом и капчей.
        :param rucaptcha_key: Ключ от RuCaptcha
        :param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        :param kwargs: Для передачи дополнительных параметров
        """
        self.service_type = service_type
        self.post_payload = {"key": rucaptcha_key, "json": 1}

        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    @api_key_check
    @service_check
    async def additional_methods(self, action: str, **kwargs):
        """
        Асинхронный метод который выполняет дополнительные действия, такие как жалобы/получение баланса и прочее.
        :param action: Тип действия, самые типичные: getbalance(получение баланса),
                                                     reportbad(жалоба на неверное решение).
        :param kwargs: Для передачи дополнительных параметров
        :return: Возвращает JSON строку с соответствующими полями:
                    serverAnswer - ответ сервера при использовании RuCaptchaControl(баланс/жалобы и т.д.),
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - название ошибки
        Больше подробностей и примеров можно прочитать в 'CaptchaTester/rucaptcha_control_example.py'
        """
        # result, url_response - задаются в декораторе `service_check`, после проверки переданного названия

        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        self.post_payload.update({"action": action})

        try:
            async with aiohttp.ClientSession() as session:
                # отправляем на сервер данные с вашим запросом
                async with session.post(self.url_response, data=self.post_payload) as resp:
                    answer = await resp.json()

        except Exception as error:
            self.result.update({"error": True, "errorBody": {"text": error, "id": -1}})
            return self.result

        if answer["status"] == 0:
            self.result.update({"error": True, "errorBody": answer["request"]})
            return self.result

        elif answer["status"] == 1:
            self.result.update({"serverAnswer": answer["request"]})
            return self.result


# Async WebSocket method
class sockRuCaptchaControl(WebSocketRuCaptcha):
    def __init__(self, rucaptcha_key: str, allSessions: bool = None, suppressSuccess: bool = None):
        """
        Method setup WebSocket connection data
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
