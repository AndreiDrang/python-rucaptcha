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
) -> dict[str, str]:
    """
    Periodically sends a synchronous request to a remote service to retrieve the result
    of a CAPTCHA-solving task.

    This function polls the service using blocking HTTP requests until the CAPTCHA is solved,
    an error is returned, or the task times out. It handles intermediate states and retries
    with a configurable sleep interval between attempts.

    Args:
        get_payload (GetTaskResultRequestSer):
            Serialized request object containing the task ID and payload data.
        sleep_time (int):
            Time in seconds to wait between polling attempts when the task is still processing.
        url_response (str):
            Endpoint URL to query for the CAPTCHA-solving result.

    Returns:
        dict[str, str]:
            A dictionary containing the final task result. If the task fails or an exception
            occurs, the dictionary includes error details such as status, errorId, errorCode,
            and errorDescription.
    """
    response_ser = GetTaskResultResponseSer(taskId=get_payload.taskId)
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
            response_ser.status = "failed"
            response_ser.errorId = 12
            response_ser.errorCode = "System error"
            response_ser.errorDescription = str(error)
    return response_ser.to_dict()


async def get_async_result(
    get_payload: GetTaskResultRequestSer, sleep_time: int, url_response: str
) -> dict[str, str]:
    """
    Periodically sends an asynchronous request to a remote service to retrieve the result
    of a CAPTCHA-solving task.

    This function polls the service at regular intervals until the CAPTCHA is solved,
    an error occurs, or the task times out. It uses aiohttp for asynchronous HTTP requests
    and handles various response states including 'processing', 'ready', and error conditions.

    Args:
        get_payload (GetTaskResultRequestSer):
            Serialized request object containing the task ID and payload data.
        sleep_time (int):
            Time in seconds to wait between polling attempts when the task is still processing.
        url_response (str):
            Endpoint URL to query for the CAPTCHA-solving result.

    Returns:
        dict[str, str]:
            A dictionary containing the final task result if successful or partially failed.
            If an exception occurs during the request, returns a dictionary with error details
            including status, errorId, errorCode, and errorDescription.
    """
    response_ser = GetTaskResultResponseSer(taskId=get_payload.taskId)
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
                response_ser.status = "failed"
                response_ser.errorId = 12
                response_ser.errorCode = "System error"
                response_ser.errorDescription = str(error)
    return response_ser.to_dict()
