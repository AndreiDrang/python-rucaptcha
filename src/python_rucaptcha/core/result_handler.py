import time
from typing import Union

import aiohttp
import requests

from .config import attempts_generator
from .serializer import GetTaskResultRequestSer, GetTaskResultResponseSer


def get_sync_result(get_payload: GetTaskResultRequestSer, sleep_time: int, url_response: str) -> Union[dict, Exception]:
    """
    Function periodically send the SYNC request to service and wait for captcha solving result
    """
    # generator for repeated attempts to connect to the server
    attempts = attempts_generator()
    for _ in attempts:
        try:
            # send a request for the result of solving the captcha
            captcha_response = GetTaskResultResponseSer(**requests.post(url_response, json=get_payload.dict()).json())
            # if the captcha has not been resolved yet, wait
            if captcha_response.status == "processing":
                time.sleep(sleep_time)
            else:
                return captcha_response.dict()

        except Exception as error:
            return error


async def get_async_result(
    get_payload: GetTaskResultRequestSer, sleep_time: int, url_response: str
) -> Union[dict, Exception]:
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
                    captcha_response = await resp.json(content_type=None)
                    captcha_response = GetTaskResultResponseSer(**captcha_response)

                    # if the captcha has not been resolved yet, wait
                    if captcha_response.status == "processing":
                        time.sleep(sleep_time)
                    else:
                        return captcha_response.dict()
            except Exception as error:
                return error
