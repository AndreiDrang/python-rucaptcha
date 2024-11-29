import time
import asyncio
import logging
from typing import Union

import aiohttp
import requests

from .config import attempts_generator
from .serializer import GetTaskResultRequestSer, GetTaskResultResponseSer


def get_sync_result(
    get_payload: GetTaskResultRequestSer, sleep_time: int, url_response: str
) -> Union[dict, Exception]:
    """
    Function periodically send the SYNC request to service and wait for captcha solving result
    """
    # generator for repeated attempts to connect to the server
    attempts = attempts_generator()
    for _ in attempts:
        try:
            # send a request for the result of solving the captcha
            captcha_response = GetTaskResultResponseSer(
                **requests.post(url_response, json=get_payload.to_dict()).json(), taskId=get_payload.taskId
            )
            logging.warning(f"{captcha_response = }")
            # if the captcha has not been resolved yet, wait
            if captcha_response.status == "processing":
                time.sleep(sleep_time)
                continue
            elif captcha_response.status == "ready":
                break
            elif captcha_response.errorId != 0:
                return captcha_response.to_dict()
        except Exception as error:
            return error
    return captcha_response.to_dict()


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
                async with session.post(
                    url_response, json=get_payload.to_dict(), raise_for_status=True
                ) as resp:
                    captcha_response = await resp.json(content_type=None)
                    captcha_response = GetTaskResultResponseSer(**captcha_response, taskId=get_payload.taskId)

                    # if the captcha has not been resolved yet, wait
                    if captcha_response.status == "processing":
                        await asyncio.sleep(sleep_time)
                        continue
                    elif captcha_response.status == "ready":
                        break
                    elif captcha_response.errorId != 0:
                        return captcha_response.to_dict()
            except Exception as error:
                return error
    return captcha_response.to_dict()
