import os
import time
import uuid
import asyncio
import logging
from typing import Union
from pathlib import Path

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from . import enums
from .config import RETRIES, ASYNC_RETRIES
from .serializer import TaskSer, CaptchaOptionsSer, CreateTaskBaseSer, CreateTaskResponseSer, GetTaskResultRequestSer
from .result_handler import get_sync_result, get_async_result


class BaseCaptcha:
    NO_CAPTCHA_ERR = "You did not send any file, local link or URL."

    def __init__(
        self,
        rucaptcha_key: str,
        method: str,
        action: str = "get",
        sleep_time: int = 15,
        service_type: str = enums.ServiceEnm.TWOCAPTCHA.value,
        **kwargs,
    ):
        """
        :param rucaptcha_key: User API key
        :param method: Captcha type
        :param action: Server action
        :param sleep_time: Time to wait for captcha solution
        :param service_type: URL with which the program will work, "2captcha" option is possible (standard)
                              and "rucaptcha"
        :param kwargs: Designed to pass OPTIONAL parameters to the payload for a request to RuCaptcha
        """
        # assign args to validator
        self.params = CaptchaOptionsSer(**locals(), **kwargs)

        # prepare create task payload
        self.create_task_payload = CreateTaskBaseSer(
            clientKey=self.params.rucaptcha_key, task=TaskSer(type=method), **locals()
        ).dict(by_alias=True)
        # prepare get task result data payload
        self.get_task_payload = GetTaskResultRequestSer(clientKey=self.params.rucaptcha_key)

        for key in kwargs:
            self.create_task_payload["task"].update({key: kwargs[key]})

        # prepare session
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=RETRIES))
        self.session.mount("https://", HTTPAdapter(max_retries=RETRIES))

    def _processing_response(self, **kwargs: dict) -> Union[dict, Exception]:
        """
        Method processing captcha solving task creation result
        :param kwargs: additional params for Requests library
        """
        logging.warning(f"{self.create_task_payload = }")
        try:
            response = CreateTaskResponseSer(
                **self.session.post(self.params.url_request, json=self.create_task_payload, **kwargs).json()
            )
            # check response status
            if response.errorId == 0:
                self.get_task_payload.taskId = response.taskId
            else:
                return response.dict()
        except Exception as error:
            return error

        # wait captcha solving
        time.sleep(self.params.sleep_time)

        return get_sync_result(
            get_payload=self.get_task_payload, sleep_time=self.params.sleep_time, url_response=self.params.url_response
        )

    def url_open(self, url: str, **kwargs):
        """
        Method open links
        """
        return self.session.get(url=url, **kwargs)

    async def aio_url_read(self, url: str, **kwargs) -> bytes:
        """
        Async method read bytes from link
        """
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.get(url=url, **kwargs) as resp:
                        return await resp.content.read()

    async def _aio_processing_response(self) -> Union[dict, Exception]:
        """
        Method processing async captcha solving task creation result
        """
        try:
            # make async or sync request
            response = await self.__aio_create_task()
            logging.warning(f"{response = }")
            # check response status
            if response.errorId == 0:
                self.get_task_payload.taskId = response.taskId
            else:
                return response.dict()
        except Exception as error:
            return error

        logging.warning(f"{self.get_task_payload = }")
        # wait captcha solving
        await asyncio.sleep(self.params.sleep_time)
        return await get_async_result(
            get_payload=self.get_task_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
        )

    async def __aio_create_task(self) -> CreateTaskResponseSer:
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.post(
                        self.params.url_request, json=self.create_task_payload, raise_for_status=True
                    ) as resp:
                        response_json = await resp.json(content_type=None)
                        return CreateTaskResponseSer(**response_json)

    # Working with images methods

    @staticmethod
    def _local_file_captcha(captcha_file: str):
        """
        Method get local file, read it and prepare for sending to Captcha solving service
        """
        with open(captcha_file, "rb") as file:
            return file.read()

    def _file_const_saver(self, content: bytes, file_path: str, file_extension: str = "png"):
        """
        Method create and save file in folder
        """
        Path(file_path).mkdir(parents=True, exist_ok=True)

        # generate image name
        self._file_name = f"file-{uuid.uuid4()}.{file_extension}"

        # save image to folder
        with open(os.path.join(file_path, self._file_name), "wb") as out_image:
            out_image.write(content)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True
