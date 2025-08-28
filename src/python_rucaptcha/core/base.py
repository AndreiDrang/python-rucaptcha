import os
import time
import uuid
import base64
import asyncio
from typing import Any, Optional
from pathlib import Path

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from .enums import ServiceEnm, SaveFormatsEnm
from .config import RETRIES, ASYNC_RETRIES
from .serializer import (
    TaskSer,
    CaptchaOptionsSer,
    CreateTaskBaseSer,
    GetTaskResultRequestSer,
    GetTaskResultResponseSer,
)
from .result_handler import get_sync_result, get_async_result


class BaseCaptcha:
    NO_CAPTCHA_ERR = "You did not send any file, local link or URL."

    def __init__(
        self,
        rucaptcha_key: str,
        method: str,
        sleep_time: int = 10,
        service_type: ServiceEnm | str = ServiceEnm.TWOCAPTCHA,
        **kwargs: dict[str, Any],
    ):
        """
        Base class for interacting with CAPTCHA-solving services such as 2Captcha and RuCaptcha.

        This class handles the setup of request payloads, session configuration, and service-specific
        parameters required to submit CAPTCHA tasks and retrieve their results. It supports optional
        customization of task parameters via keyword arguments and includes retry logic for HTTP requests.

        Args:
            rucaptcha_key (str):
                API key provided by the CAPTCHA-solving service.
            method (str):
                Type of CAPTCHA to solve (e.g., "ImageToText", "ReCaptchaV2").
            sleep_time (int, optional):
                Time in seconds to wait between polling attempts. Defaults to 10.
            service_type (ServiceEnm | str, optional):
                Service provider to use. Accepts `ServiceEnm.TWOCAPTCHA` or `"rucaptcha"`. Defaults to TWOCAPTCHA.
            **kwargs (dict[str, Any]):
                Optional parameters to be injected into the task payload (e.g., `websiteURL`, `siteKey`, `proxy`).

        Example:
            >>> captcha = BaseCaptcha("your-api-key", method="ReCaptchaV2", websiteURL="https://example.com", siteKey="abc123")
            >>> captcha.create_task_payload
            {'clientKey': 'your-api-key', 'task': {'type': 'ReCaptchaV2', 'websiteURL': 'https://example.com', 'siteKey': 'abc123'}}
        """
        self.result = GetTaskResultResponseSer()
        # assign args to validator
        self.params = CaptchaOptionsSer(sleep_time=sleep_time, service_type=service_type)
        self.params.urls_set()

        # prepare create task payload
        self.create_task_payload = CreateTaskBaseSer(
            clientKey=rucaptcha_key, task=TaskSer(type=method)
        ).to_dict()
        # prepare get task result data payload
        self.get_task_payload = GetTaskResultRequestSer(clientKey=rucaptcha_key)

        for key in kwargs:
            self.create_task_payload["task"].update({key: kwargs[key]})

        # prepare session
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=RETRIES))
        self.session.mount("https://", HTTPAdapter(max_retries=RETRIES))

    def _processing_response(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Method processing captcha solving task creation result
        :param kwargs: additional params for Requests library
        """
        try:
            response = GetTaskResultResponseSer(
                **self.session.post(self.params.url_request, json=self.create_task_payload, **kwargs).json()
            )
            # check response status
            if response.errorId == 0:
                self.get_task_payload.taskId = response.taskId
            else:
                return response.to_dict()
        except Exception as error:
            self.result.errorId = 12
            self.result.errorCode = self.NO_CAPTCHA_ERR
            self.result.errorDescription = str(error)
            return self.result.to_dict()

        # wait captcha solving
        time.sleep(self.params.sleep_time)

        return get_sync_result(
            get_payload=self.get_task_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
        )

    def url_open(self, url: str, **kwargs: dict[str, Any]):
        """
        Method open links
        """
        return self.session.get(url=url, **kwargs)

    async def aio_url_read(self, url: str, **kwargs: dict[str, Any]) -> bytes | None:
        """
        Async method read bytes from link
        """
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.get(url=url, **kwargs) as resp:
                        return await resp.content.read()

    async def _aio_processing_response(self) -> dict[str, Any]:
        """
        Method processing async captcha solving task creation result
        """
        try:
            # make async or sync request
            response = await self.__aio_create_task()
            # check response status
            if response.errorId == 0:
                self.get_task_payload.taskId = response.taskId
            else:
                return response.to_dict()
        except Exception as error:
            self.result.errorId = 12
            self.result.errorCode = self.NO_CAPTCHA_ERR
            self.result.errorDescription = str(error)
            return self.result.to_dict()

        # wait captcha solving
        await asyncio.sleep(self.params.sleep_time)
        return await get_async_result(
            get_payload=self.get_task_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
        )

    async def __aio_create_task(self) -> GetTaskResultResponseSer:
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.post(
                        self.params.url_request, json=self.create_task_payload, raise_for_status=True
                    ) as resp:
                        response_json = await resp.json(content_type=None)
                        return GetTaskResultResponseSer(**response_json)

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

    def _body_file_processing(
        self,
        save_format: SaveFormatsEnm | str,
        file_path: str,
        file_extension: str = "png",
        image_key: str = "body",
        captcha_link: str | None = None,
        captcha_file: str | None = None,
        captcha_base64: bytes | None = None,
        **kwargs: dict[str, Any],
    ):
        # if a local file link is passed
        if captcha_file:
            self.create_task_payload["task"].update(
                {image_key: base64.b64encode(self._local_file_captcha(captcha_file)).decode("utf-8")}
            )
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.create_task_payload["task"].update(
                {image_key: base64.b64encode(captcha_base64).decode("utf-8")}
            )
        # if a URL is passed
        elif captcha_link:
            try:
                content = self.url_open(url=captcha_link, **kwargs).content
                # according to the value of the passed parameter, select the function to save the image
                if save_format == SaveFormatsEnm.CONST.value:
                    self._file_const_saver(content, file_path, file_extension=file_extension)
                self.create_task_payload["task"].update(
                    {image_key: base64.b64encode(content).decode("utf-8")}
                )
            except Exception as error:
                self.result.errorId = 12
                self.result.errorCode = self.NO_CAPTCHA_ERR
                self.result.errorDescription = str(error)

        else:
            self.result.errorId = 12
            self.result.errorCode = self.NO_CAPTCHA_ERR

    async def _aio_body_file_processing(
        self,
        save_format: SaveFormatsEnm | str,
        file_path: str,
        file_extension: str = "png",
        image_key: str = "body",
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        **kwargs: dict[str, Any],
    ):
        # if a local file link is passed
        if captcha_file:
            self.create_task_payload["task"].update(
                {image_key: base64.b64encode(self._local_file_captcha(captcha_file)).decode("utf-8")}
            )
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.create_task_payload["task"].update(
                {image_key: base64.b64encode(captcha_base64).decode("utf-8")}
            )
        # if a URL is passed
        elif captcha_link:
            try:
                content = await self.aio_url_read(url=captcha_link, **kwargs)
                # according to the value of the passed parameter, select the function to save the image
                if save_format == SaveFormatsEnm.CONST.value:
                    self._file_const_saver(content, file_path, file_extension=file_extension)
                self.create_task_payload["task"].update(
                    {image_key: base64.b64encode(content).decode("utf-8")}
                )
            except Exception as error:
                self.result.errorId = 12
                self.result.errorCode = self.NO_CAPTCHA_ERR
                self.result.errorDescription = str(error)

        else:
            self.result.errorId = 12
            self.result.errorCode = self.NO_CAPTCHA_ERR

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
