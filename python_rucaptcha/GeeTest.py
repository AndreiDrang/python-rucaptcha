import time
import asyncio

import aiohttp

from .base import BaseCaptcha
from .serializer import ServicePostResponseSer
from .result_handler import get_sync_result, get_async_result


class GeeTest(BaseCaptcha):
    """
    Модуль отвечает за решение Geetest и Geetest v4
    Подробнее о параметрах:
        https://rucaptcha.com/api-rucaptcha#solving_geetest
        https://rucaptcha.com/api-rucaptcha#geetest-v4
    """

    def captcha_handler(self, challenge: str = None, **kwargs):
        """
        Метод отвечает за передачу данных на сервер для решения капчи
        :param challenge: Значение параметра challenge найденное на сайте
        :param kwargs: Параметры для библиотеки `requests`
        :return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    taskId - находится Id задачи на решение капчи,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - название ошибки
        """
        self.post_payload.update({"challenge": challenge})
        try:
            response = ServicePostResponseSer(
                **self.session.post(self.params.url_request, data=self.post_payload, **kwargs).json()
            )
            if response.status == 1:
                self.result.taskId = response.request
            else:
                self.result.error = True
                self.result.errorBody = response.request
        except Exception as error:
            self.result.error = True
            self.result.errorBody = error

        # check for errors when downloading / transferring a file to the server
        if self.result.error:
            return self.result.dict(exclude_none=True)
        # if all is ok - send captcha to service and wait solution
        else:
            # update payload - add captcha taskId
            self.get_payload.update({"id": self.result.taskId})

            # wait captcha solving
            time.sleep(self.params.sleep_time)
            return get_sync_result(
                get_payload=self.get_payload,
                sleep_time=self.params.sleep_time,
                url_response=self.params.url_response,
                result=self.result,
            )


class aioGeeTest(BaseCaptcha):
    """
    Модуль отвечает за асинхронное решение Geetest и Geetest v4
    Подробнее о параметрах:
        https://rucaptcha.com/api-rucaptcha#solving_geetest
        https://rucaptcha.com/api-rucaptcha#geetest-v4
    """

    async def captcha_handler(self, challenge: str = None):
        """
        Метод отвечает за передачу данных на сервер для решения капчи
        :param challenge: Значение параметра challenge найденное на сайте
        :param proxy: Прокси для aiohttp модуля
        :return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    taskId - находится Id задачи на решение капчи,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - название ошибки
        """
        self.post_payload.update({"challenge": challenge})
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.params.url_request, data=self.post_payload) as resp:
                    response_json = await resp.json()
                    response = ServicePostResponseSer(**response_json)

            if response.status == 1:
                self.result.taskId = response.request
            else:
                self.result.error = True
                self.result.errorBody = response.request

        except Exception as error:
            self.result.error = True
            self.result.errorBody = error

        # check for errors when downloading / transferring a file to the server
        if self.result.error:
            return self.result.dict(exclude_none=True)
        # if all is ok - send captcha to service and wait solution
        else:
            # update payload - add captcha taskId
            self.get_payload.update({"id": self.result.taskId})

            # wait captcha solving
            await asyncio.sleep(self.params.sleep_time)
            return await get_async_result(
                get_payload=self.get_payload,
                sleep_time=self.params.sleep_time,
                url_response=self.params.url_response,
                result=self.result,
            )
