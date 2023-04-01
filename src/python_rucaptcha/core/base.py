import os
import time
import uuid
import asyncio
from pathlib import Path

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from . import enums
from .config import RETRIES, ASYNC_RETRIES
from .serializer import ResponseSer, GetRequestSer, PostRequestSer, CaptchaOptionsSer, ServicePostResponseSer
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

        # prepare POST payload
        self.post_payload = PostRequestSer(key=self.params.rucaptcha_key, method=method).dict(by_alias=True)
        # prepare GET payload
        self.get_payload = GetRequestSer(key=self.params.rucaptcha_key, action=action).dict(
            by_alias=True, exclude_none=True
        )
        # prepare result payload
        self.result = ResponseSer()

        for key in kwargs:
            self.post_payload.update({key: kwargs[key]})

        # prepare session
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=RETRIES))
        self.session.mount("https://", HTTPAdapter(max_retries=RETRIES))

    def _processing_response(self, **kwargs: dict) -> dict:
        """
        Method processing captcha solving task creation result
        :param kwargs: additional params for Requests library
        """
        try:
            response = ServicePostResponseSer(
                **self.session.post(self.params.url_request, data=self.post_payload, **kwargs).json()
            )
            # check response status
            if response.status == 1:
                self.result.taskId = response.request
            else:
                self.result.error = True
                self.result.errorBody = response.request
        except Exception as error:
            self.result.error = True
            self.result.errorBody = str(error)

        # check for errors while make request to server
        if self.result.error:
            return self.result.dict()

        # if all is ok - send captcha to service and wait solution
        # update payload - add captcha taskId
        self.get_payload.update({"id": self.result.taskId})

        # wait captcha solving
        time.sleep(self.params.sleep_time)
        return get_sync_result(
            get_payload=self.get_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
            result=self.result,
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

    async def _aio_processing_response(self) -> dict:
        """
        Method processing async captcha solving task creation result
        """
        try:
            # make async or sync request
            response = await self.__aio_make_post_request()
            # check response status
            if response.status == 1:
                self.result.taskId = response.request
            else:
                self.result.error = True
                self.result.errorBody = response.request
        except Exception as error:
            self.result.error = True
            self.result.errorBody = str(error)

        # check for errors while make request to server
        if self.result.error:
            return self.result.dict()

        # if all is ok - send captcha to service and wait solution
        # update payload - add captcha taskId
        self.get_payload.update({"id": self.result.taskId})

        # wait captcha solving
        await asyncio.sleep(self.params.sleep_time)
        return await get_async_result(
            get_payload=self.get_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
            result=self.result,
        )

    async def __aio_make_post_request(self) -> ServicePostResponseSer:
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.post(
                        self.params.url_request, data=self.post_payload, raise_for_status=True
                    ) as resp:
                        response_json = await resp.json()
                        return ServicePostResponseSer(**response_json)

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
