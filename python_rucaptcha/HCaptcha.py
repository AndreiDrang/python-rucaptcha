import time
import asyncio

import aiohttp
import requests

from python_rucaptcha.config import app_key
from python_rucaptcha.decorators import api_key_check, service_check
from python_rucaptcha.result_handler import get_sync_result, get_async_result


class HCaptcha:
    """
    The class is used to work with HCaptcha.
    """

    def __init__(
        self,
        rucaptcha_key,
        service_type: str = "2captcha",
        sleep_time: int = 10,
        proxy: str = None,
        proxytype: str = None,
        pingback: str = None,
        **kwargs,
    ):
        """
        Initialization of the necessary variables.
        : param rucaptcha_key: API captcha key from user account
        : param service_type: URL with which the program will work, the option "2captcha" (standard) is possible
                                     and "rucaptcha"
        : param sleep_time: Verma waiting for a captcha solution
        : param proxy: To solve recaptcha through a proxy, proxies and authentication data are transmitted.
                        `login: password@IP_address:PORT` /` login: password @ IP: port`.
        : param proxytype: The type of proxy to use. Available: `HTTP`,` HTTPS`, `SOCKS4`,` SOCKS5`.
        : param pingback: Parameter for the link with which there will be a wait for a callback response from RuCaptcha
        : param kwargs: To pass additional parameters
        """
        # время ожидания решения капчи
        self.sleep_time = sleep_time
        # тип URL на с которым будет работать библиотека
        self.service_type = service_type
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {
            "key": rucaptcha_key,
            "method": "hcaptcha",
            "json": 1,
            "soft_id": app_key,
        }

        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        # если был передан параметр для callback`a - добавляем его
        if pingback:
            self.post_payload.update({"pingback": pingback})

        # добавление прокси для решения капчи с того же IP
        if proxy and proxytype:
            self.post_payload.update({"proxy": proxy, "proxytype": proxytype})

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {"key": rucaptcha_key, "action": "get", "json": 1}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    @api_key_check
    @service_check
    def captcha_handler(self, site_key: str, page_url: str, **kwargs):
        """
        The method is responsible for transferring data to the server to solve captcha
        : param site_key: Website sitekey
        : param page_url: Link to the page where the captcha is located
        : param kwargs: To pass additional parameters
        : return: Answer to the captcha as a JSON string with fields:
                    captchaSolve - captcha solution,
                    taskId - is the Id of the task to solve the captcha, can be used for complaints and other things,
                    error - False - if everything is fine, True - if there is an error,
                    errorBody - full error information:
                        {
                            text - Extended error explanation
                            id - unique error number in THIS library
                        }
        """
        # result, url_request, url_response - задаются в декораторе `service_check`, после проверки переданного названия

        # Если переданы ещё параметры - вносим их в get_payload
        if kwargs:
            for key in kwargs:
                self.get_payload.update({key: kwargs[key]})

        self.post_payload.update({"sitekey": site_key, "pageurl": page_url})
        # получаем ID капчи
        captcha_id = requests.post(self.url_request, data=self.post_payload).json()

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id["status"] == 0:
            self.result.update({"error": True, "errorBody": captcha_id["request"]})
            return self.result
        # иначе берём ключ отправленной на решение капчи и ждём решения
        else:
            captcha_id = captcha_id["request"]
            # вписываем в taskId ключ отправленной на решение капчи
            self.result.update({"taskId": captcha_id})
            # обновляем пайлоад, вносим в него ключ отправленной на решение капчи
            self.get_payload.update({"id": captcha_id})

            # если передан параметр `pingback` - не ждём решения капчи а возвращаем незаполненный ответ
            if self.post_payload.get("pingback"):
                return self.get_payload

            else:
                # Ожидаем решения капчи 10 секунд
                time.sleep(self.sleep_time)
                return get_sync_result(
                    get_payload=self.get_payload,
                    sleep_time=self.sleep_time,
                    url_response=self.url_response,
                    result=self.result,
                )


class aioHCaptcha:
    """
    The class is used to work with HCaptcha.
    """

    def __init__(
        self,
        rucaptcha_key: str,
        service_type: str = "2captcha",
        sleep_time: int = 10,
        proxy: str = None,
        proxytype: str = None,
        pingback: str = None,
        **kwargs,
    ):
        """
        Initialization of the necessary variables.
        : param rucaptcha_key: API captcha key from user account
        : param service_type: URL with which the program will work, the option "2captcha" (standard) is possible
                                     and "rucaptcha"
        : param sleep_time: Verma waiting for a captcha solution
        : param proxy: To solve recaptcha through a proxy, proxies and authentication data are transmitted.
                        `login: password@IP_address:PORT` /` login: password @ IP: port`.
        : param proxytype: The type of proxy to use. Available: `HTTP`,` HTTPS`, `SOCKS4`,` SOCKS5`.
        : param pingback: Parameter for the link with which there will be a wait for a callback response from RuCaptcha
        : param kwargs: To pass additional parameters
        """
        # время ожидания решения капчи
        self.sleep_time = sleep_time
        # тип URL на с которым будет работать библиотека
        self.service_type = service_type
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {
            "key": rucaptcha_key,
            "method": "hcaptcha",
            "json": 1,
            "soft_id": app_key,
        }

        # добавление прокси для решения капчи с того же IP
        if proxy and proxytype:
            self.post_payload.update({"proxy": proxy, "proxytype": proxytype})

        # если был передан параметр для callback`a - добавляем его
        if pingback:
            self.post_payload.update({"pingback": pingback})

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {"key": rucaptcha_key, "action": "get", "json": 1}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    # Работа с капчей
    @api_key_check
    @service_check
    async def captcha_handler(self, site_key: str, page_url: str, **kwargs):
        """
        The method is responsible for transferring data to the server to solve captcha
        : param site_key: Website sitekey
        : param page_url: Link to the page where the captcha is located
        : param kwargs: To pass additional parameters
        : return: Answer to the captcha as a JSON string with fields:
                    captchaSolve - captcha solution,
                    taskId - is the Id of the task to solve the captcha, can be used for complaints and other things,
                    error - False - if everything is fine, True - if there is an error,
                    errorBody - full error information:
                        {
                            text - Extended error explanation
                            id - unique error number in THIS library
                        }
        """
        # result, url_request, url_response - задаются в декораторе `service_check`, после проверки переданного названия

        # Если переданы ещё параметры - вносим их в get_payload
        if kwargs:
            for key in kwargs:
                self.get_payload.update({key: kwargs[key]})

        self.post_payload.update({"sitekey": site_key, "pageurl": page_url})
        # получаем ID капчи
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url_request, data=self.post_payload) as resp:
                captcha_id = await resp.json()

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id["status"] == 0:
            self.result.update({"error": True, "errorBody": captcha_id["request"]})
            return self.result
        # иначе берём ключ отправленной на решение капчи и ждём решения
        else:
            captcha_id = captcha_id["request"]
            # вписываем в taskId ключ отправленной на решение капчи
            self.result.update({"taskId": captcha_id})
            # обновляем пайлоад, вносим в него ключ отправленной на решение капчи
            self.get_payload.update({"id": captcha_id})

            # если передан параметр `pingback` - не ждём решения капчи а возвращаем незаполненный ответ
            if self.post_payload.get("pingback"):
                return self.get_payload

            else:
                # Ожидаем решения капчи
                await asyncio.sleep(self.sleep_time)
                return await get_async_result(
                    get_payload=self.get_payload,
                    sleep_time=self.sleep_time,
                    url_response=self.url_response,
                    result=self.result,
                )
