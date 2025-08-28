import time
import asyncio
import logging
from typing import Any

import aiohttp
import requests

from .config import attempts_generator
from .serializer import GetTaskResultRequestSer, GetTaskResultResponseSer


def get_sync_result(
    get_payload: GetTaskResultRequestSer, sleep_time: int, url_response: str
) -> dict[str, str] | Exception:
    """
    Function periodically send the SYNC request to service and wait for captcha solving result
    """
    # generator for repeated attempts to connect to the server
    attempts = attempts_generator()
    for _ in attempts:
        try:
            # send a request for the result of solving the captcha
            result: dict[str, Any] = requests.post(url_response, json=get_payload.to_dict()).json()
            logging.info(f"Received captcha sync result - {result = }")
            response_ser = GetTaskResultResponseSer(**result, taskId=get_payload.taskId)
            # if the captcha has not been resolved yet, wait
            if response_ser.status == "processing":
                time.sleep(sleep_time)
                continue
            elif response_ser.status == "ready":
                break
            elif response_ser.errorId != 0:
                return response_ser.to_dict()
        except Exception as error:
            return error
    return response_ser.to_dict()


async def get_async_result(
    get_payload: GetTaskResultRequestSer, sleep_time: int, url_response: str
) -> dict[str, str] | Exception:
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
                    result: dict[str, Any] = await resp.json(content_type=None)
                    logging.info(f"Received captcha async result - {result = }")
                    response_ser = GetTaskResultResponseSer(**result, taskId=get_payload.taskId)

                    # if the captcha has not been resolved yet, wait
                    if response_ser.status == "processing":
                        await asyncio.sleep(sleep_time)
                        continue
                    elif response_ser.status == "ready":
                        break
                    elif response_ser.errorId != 0:
                        return response_ser.to_dict()
            except Exception as error:
                return error
    return response_ser.to_dict()
