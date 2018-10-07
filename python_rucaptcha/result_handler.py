import requests
import time
import aiohttp
import asyncio

from urllib3.exceptions import MaxRetryError

from .config import connect_generator
from .errors import RuCaptchaError


# синхронный метод
def get_sync_result(get_payload: dict, sleep_time: int, url_response: str, result: dict):
    # генератор для повторных попыток подключения к серверу получения решения капчи
    connect_gen = connect_generator()
    while True:
        try:
            # отправляем запрос на результат решения капчи, если не решена ожидаем
            captcha_response = requests.post(url_response, data = get_payload)

            # если капча ещё не решена - ожидаем
            if captcha_response.json()['request'] == 'CAPCHA_NOT_READY':
                time.sleep(sleep_time)

            # при ошибке во время решения
            elif captcha_response.json()["status"] == 0:
                result.update({'error': 1,
                               'errorBody': RuCaptchaError().errors(captcha_response.json()["request"])
                               }
                              )
                return result

            # при решении капчи
            elif captcha_response.json()["status"] == 1:
                result.update({'captchaSolve': captcha_response.json()['request']})
                return result

        except Exception as error:
                if next(connect_gen) < 4:
                    time.sleep(2)
                else:
                    result.update({'error': True,
                                   'errorBody': {
                                       'text': error,
                                       'id': -1
                                   }
                                   }
                                  )
                    return result


# асинхронный метод
async def get_async_result(get_payload: dict, sleep_time: int, url_response: str, result: dict):
    # генератор для повторных попыток подключения к серверу получения решения капчи
    connect_gen = connect_generator()
    # отправляем запрос на результат решения капчи, если не решена ожидаем
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.post(url_response, data = get_payload) as resp:
                    captcha_response = await resp.json()

                    # если капча ещё не решена - ожидаем
                    if captcha_response['request'] == 'CAPCHA_NOT_READY':
                        await asyncio.sleep(sleep_time)

                    # при ошибке во время решения
                    elif captcha_response["status"] == 0:
                        result.update({'error': True,
                                       'errorBody': RuCaptchaError().errors(captcha_response["request"])
                                       }
                                      )
                        return result

                    # при решении капчи
                    elif captcha_response["status"] == 1:
                        result.update({
                            'captchaSolve': captcha_response['request']
                        }
                        )
                        return result

            except Exception as error:
                if next(connect_gen) < 4:
                    time.sleep(2)
                else:
                    result.update({'error': True,
                                   'errorBody': {
                                       'text': error,
                                       'id': -1
                                   }
                                   }
                                  )
                    return result
