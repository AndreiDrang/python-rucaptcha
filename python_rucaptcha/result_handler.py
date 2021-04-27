import time
import asyncio

import aiohttp
import requests

from .config import connect_generator
from .serializer import ResponseSer, ServiceGetResponseSer


def get_sync_result(get_payload: dict, sleep_time: int, url_response: str, result: ResponseSer) -> dict:
    # генератор для повторных попыток подключения к серверу
    connect_gen = connect_generator()
    while True:
        try:
            # отправляем запрос на результат решения капчи
            captcha_response = ServiceGetResponseSer(**requests.get(url_response, params=get_payload).json())
            # если капча ещё не решена - ожидаем
            if captcha_response.request == "CAPCHA_NOT_READY":
                time.sleep(sleep_time)

            # при ошибке во время решения
            elif captcha_response.status == 0:
                result.error = True
                result.errorBody = captcha_response.request
                return result.dict()

            # при решении капчи
            elif captcha_response.status == 1:
                result.captchaSolve = captcha_response.request

                # если это ReCaptcha v3 то получаем от сервера
                # дополнительные поля, с ID юзера и его счётом
                if captcha_response.user_check and captcha_response.user_score:
                    result = result.dict()
                    result.update(
                        {
                            "user_check": captcha_response.user_check,
                            "user_score": captcha_response.user_score,
                        }
                    )

                return result

        except Exception as error:
            if next(connect_gen) < 4:
                time.sleep(2)
            else:
                result.error = True
                result.errorBody = error
                return result.dict()


async def get_async_result(get_payload: dict, sleep_time: int, url_response: str, result: dict):
    # генератор для повторных попыток подключения к серверу
    connect_gen = connect_generator()
    # отправляем запрос на результат решения капчи, если не решена ожидаем
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url_response, params=get_payload) as resp:
                    captcha_response = await resp.json()

                    # если капча ещё не решена - ожидаем
                    if captcha_response["request"] == "CAPCHA_NOT_READY":
                        await asyncio.sleep(sleep_time)

                    # при ошибке во время решения
                    elif captcha_response["status"] == 0:
                        result.update(
                            {
                                "error": True,
                                "errorBody": captcha_response["request"],
                            }
                        )
                        return result

                    # при решении капчи
                    elif captcha_response["status"] == 1:
                        result.update({"captchaSolve": captcha_response["request"]})

                        # если это ReCaptcha v3 то получаем от сервера
                        # дополнительные поля, с ID юзера и его счётом
                        if captcha_response.get("user_check") and captcha_response.get("user_score"):
                            result.update(
                                {
                                    "user_check": captcha_response.get("user_check"),
                                    "user_score": captcha_response.get("user_score"),
                                }
                            )
                        return result

            except Exception as error:
                if next(connect_gen) < 4:
                    await asyncio.sleep(2)
                else:
                    result.update({"error": True, "errorBody": {"text": error, "id": -1}})
                    return result
