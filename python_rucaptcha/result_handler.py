import requests
import time
import aiohttp
import asyncio

from urllib3.exceptions import MaxRetryError

from .errors import RuCaptchaError


# синхронный метод
def get_sync_result(get_payload: dict, sleep_time: int, url_response: str, result: dict):
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

        except (TimeoutError, ConnectionError, MaxRetryError) as error:
            result.update({'error': True,
                           'errorBody': {
                               'text': error,
                               'id': -1
                           }
                           }
                          )
            return result

        except Exception as error:
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
                result.update({'error': True,
                               'errorBody': {
                                   'text': error,
                                   'id': -1
                               }
                               }
                              )
                return result
