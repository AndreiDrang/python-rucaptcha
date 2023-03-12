import time
import asyncio

import aiohttp
import requests

from .config import attempts_generator
from .serializer import ResponseSer, ServiceGetResponseSer


def result_processing(captcha_response: ServiceGetResponseSer, result: ResponseSer) -> dict:
    """
    Function processing service response status values
    """

    # on error during solving
    if captcha_response.status == 0:
        result.error = True
        result.errorBody = captcha_response.request

    # if solving is success
    elif captcha_response.status == 1:
        result.error = False
        result.errorBody = None
        result.captchaSolve = captcha_response.request

        # if this is ReCaptcha v3 then we get it from the server
        if captcha_response.user_check and captcha_response.user_score:
            result = result.dict()
            result.update(
                {
                    "user_check": captcha_response.user_check,
                    "user_score": captcha_response.user_score,
                }
            )
            return result

    return result.dict()


def get_sync_result(get_payload: dict, sleep_time: int, url_response: str, result: ResponseSer) -> dict:
    """
    Function periodically send the SYNC request to service and wait for captcha solving result
    """
    # generator for repeated attempts to connect to the server
    attempts = attempts_generator()
    for _ in attempts:
        try:
            # send a request for the result of solving the captcha
            captcha_response = ServiceGetResponseSer(**requests.get(url_response, params=get_payload).json())
            # if the captcha has not been resolved yet, wait
            if captcha_response.request == "CAPCHA_NOT_READY":
                time.sleep(sleep_time)
                result.error = True
                result.errorBody = "ERROR_CAPTCHA_UNSOLVABLE"
            else:
                return result_processing(captcha_response, result)

        except Exception as error:
            result.error = True
            result.errorBody = error

    return result.dict()


async def get_async_result(get_payload: dict, sleep_time: int, url_response: str, result: ResponseSer) -> dict:
    """
    Function periodically send the ASYNC request to service and wait for captcha solving result
    """
    # generator for repeated attempts to connect to the server
    attempts = attempts_generator()
    async with aiohttp.ClientSession() as session:
        for _ in attempts:
            try:
                # send a request for the result of solving the captcha
                async with session.get(url_response, params=get_payload, raise_for_status=True) as resp:
                    captcha_response = await resp.json()
                    captcha_response = ServiceGetResponseSer(**captcha_response)

                    # if the captcha has not been resolved yet, wait
                    if captcha_response.request == "CAPCHA_NOT_READY":
                        await asyncio.sleep(sleep_time)
                        result.error = True
                        result.errorBody = "ERROR_CAPTCHA_UNSOLVABLE"

                    else:
                        return result_processing(captcha_response, result)

            except Exception as error:
                result.error = True
                result.errorBody = error
    return result.dict()
