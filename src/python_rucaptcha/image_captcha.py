import base64
import shutil
from typing import Optional

from .core.base import BaseCaptcha
from .core.enums import SaveFormatsEnm, ImageCaptchaEnm
from .core.serializer import GetTaskResultResponseSer


class ImageCaptcha(BaseCaptcha):
    def __init__(
        self,
        save_format: str = SaveFormatsEnm.TEMP.value,
        img_clearing: bool = True,
        img_path: str = "PythonRuCaptchaImages",
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Image Captcha.

        Args:
            rucaptcha_key: User API key
            save_format: The format in which the image will be saved, or as a temporary file - 'temp',
                                 or as a regular image to a folder created by the library - 'const'.
            img_clearing: True - delete file after solution, False - don't delete file after solution
            img_path: Folder to save captcha images
            kwargs: Additional not required params for this captcha type

        Examples:
            >>> ImageCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).captcha_handler(captcha_link="https://rucaptcha.com/dist/web/99581b9d446a509a0a01954438a5e36a.jpg")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "text":"w9h5k"
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            >>> ImageCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).captcha_handler(captcha_file="src/examples/088636.png")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "text":"w9h5k"
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            >>> with open("src/examples/088636.png", "rb") as f:
            ...     file_data = f.read()
            >>> ImageCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122"
            ...             ).captcha_handler(captcha_base64=file_data)
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "text":"w9h5k"
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            >>> await ImageCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).aio_captcha_handler(captcha_link="https://rucaptcha.com/dist/web/99581b9d446a509a0a01954438a5e36a.jpg")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "text":"w9h5k"
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            >>> await ImageCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).aio_captcha_handler(captcha_file="src/examples/088636.png")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "text":"w9h5k"
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            Death Captcha

            >>> ImageCaptcha(rucaptcha_key="some_username:some_password",
            ...             service_type="deathbycaptcha"
            ...             ).captcha_handler(captcha_file="src/examples/088636.jpg")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "text":"w9h5k"
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            >>> await ImageCaptcha(rucaptcha_key="some_username:some_password",
            ...             service_type="deathbycaptcha"
            ...             ).aio_captcha_handler(captcha_link="https://rucaptcha.com/dist/web/99581b9d446a509a0a01954438a5e36a.jpg")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "text":"w9h5k"
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            >>> with open("src/examples/088636.png", "rb") as f:
            ...     file_data = f.read()
            >>> await ImageCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122"
            ...             ).aio_captcha_handler(captcha_base64=file_data)
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "text":"w9h5k"
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

        Returns:
            Dict with full server response

        Notes:
            https://2captcha.com/api-docs/normal-captcha

            https://rucaptcha.com/api-docs/normal-captcha
        """
        super().__init__(method=ImageCaptchaEnm.ImageToTextTask.value, *args, **kwargs)

        self.save_format = save_format
        self.img_clearing = img_clearing
        self.img_path = img_path
        self.result = GetTaskResultResponseSer()

    def captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        **kwargs,
    ) -> dict:
        """
        Sync solving method

        Args:
            captcha_link: Captcha image URL
            captcha_file: Captcha image file path
            captcha_base64: Captcha image BASE64 info
            kwargs: additional params for `requests` library

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        # if a local file link is passed
        if captcha_file:
            self.create_task_payload["task"].update(
                {"body": base64.b64encode(self._local_file_captcha(captcha_file)).decode("utf-8")}
            )
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.create_task_payload["task"].update({"body": base64.b64encode(captcha_base64).decode("utf-8")})
        # if a URL is passed
        elif captcha_link:
            try:
                content = self.url_open(url=captcha_link, **kwargs).content
            except Exception as error:
                self.result.errorId = 12
                self.result.solution = {"text": str(error)}
                return self.result.to_dict()

            # according to the value of the passed parameter, select the function to save the image
            if self.save_format == SaveFormatsEnm.CONST.value:
                self._file_const_saver(content, self.img_path)
            self.create_task_payload["task"].update({"body": base64.b64encode(content).decode("utf-8")})

        else:
            # if none of the parameters are passed
            self.result.errorId = 12
            self.result.solution = {"text": "No captcha send"}
            return self.result.to_dict()

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        **kwargs,
    ) -> dict:
        """
        Async solving method

        Args:
            captcha_link: Captcha image URL
            captcha_file: Captcha image file path
            captcha_base64: Captcha image BASE64 info
            kwargs: additional params for `aiohttp` library

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        # if a local file link is passed
        if captcha_file:
            self.create_task_payload["task"].update(
                {"body": base64.b64encode(self._local_file_captcha(captcha_file)).decode("utf-8")}
            )
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.create_task_payload["task"].update({"body": base64.b64encode(captcha_base64).decode("utf-8")})
        # if a URL is passed
        elif captcha_link:
            try:
                content = await self.aio_url_read(url=captcha_link, **kwargs)
            except Exception as error:
                self.result.errorId = 12
                self.result.solution = {"text": str(error)}
                return self.result.to_dict()

            # according to the value of the passed parameter, select the function to save the image
            if self.save_format == SaveFormatsEnm.CONST.value:
                self._file_const_saver(content, self.img_path)
            self.create_task_payload["task"].update({"body": base64.b64encode(content).decode("utf-8")})

        else:
            # if none of the parameters are passed
            self.result.errorId = 12
            self.result.solution = {"text": "No captcha send"}
            return self.result.to_dict()

        return await self._aio_processing_response()

    def __del__(self):
        if self.save_format == SaveFormatsEnm.CONST.value and self.img_clearing:
            shutil.rmtree(self.img_path)
