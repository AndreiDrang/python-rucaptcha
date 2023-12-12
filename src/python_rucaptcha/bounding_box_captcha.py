import shutil
import logging
from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enums import SaveFormatsEnm, BoundingBoxCaptchaEnm


class BoundingBoxCaptcha(BaseCaptcha):
    def __init__(
        self,
        save_format: Union[str, SaveFormatsEnm] = SaveFormatsEnm.TEMP,
        img_clearing: bool = True,
        img_path: str = "PythonRuCaptchaBoundingBox",
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Bounding Box.

        Args:
            rucaptcha_key: User API key
            save_format: The format in which the image will be saved, or as a temporary file - 'temp',
                                 or as a regular image to a folder created by the library - 'const'.
            img_clearing: True - delete file after solution, False - don't delete file after solution
            img_path: Folder to save captcha images
            kwargs: Additional not required params for this captcha type

        Examples:
            >>> BoundingBoxCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).captcha_handler(captcha_link="https://rucaptcha.com/dist/web/99581b9d446a509a0a01954438a5e36a.jpg")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "bounding_boxes": [
                        {
                            "xMin": 310,
                            "xMax": 385,
                            "yMin": 231,
                            "yMax": 308
                        }
                    ]
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            >>> BoundingBoxCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).captcha_handler(captcha_file="src/examples/088636.png")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "bounding_boxes": [
                        {
                            "xMin": 310,
                            "xMax": 385,
                            "yMin": 231,
                            "yMax": 308
                        }
                    ]
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
            >>> BoundingBoxCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122"
            ...             ).captcha_handler(captcha_base64=file_data)
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "bounding_boxes": [
                        {
                            "xMin": 310,
                            "xMax": 385,
                            "yMin": 231,
                            "yMax": 308
                        }
                    ]
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            >>> await BoundingBoxCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).aio_captcha_handler(captcha_link="https://rucaptcha.com/dist/web/99581b9d446a509a0a01954438a5e36a.jpg")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "bounding_boxes": [
                        {
                            "xMin": 310,
                            "xMax": 385,
                            "yMin": 231,
                            "yMax": 308
                        }
                    ]
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            >>> await BoundingBoxCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).aio_captcha_handler(captcha_file="src/examples/088636.png")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "bounding_boxes": [
                        {
                            "xMin": 310,
                            "xMax": 385,
                            "yMin": 231,
                            "yMax": 308
                        }
                    ]
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            Death Captcha

            >>> BoundingBoxCaptcha(rucaptcha_key="some_username:some_password",
            ...             service_type="deathbycaptcha"
            ...             ).captcha_handler(captcha_file="src/examples/088636.jpg")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "bounding_boxes": [
                        {
                            "xMin": 310,
                            "xMax": 385,
                            "yMin": 231,
                            "yMax": 308
                        }
                    ]
               },
               "cost":0.033,
               "ip":"46.53.241.91",
               "createTime":1696730723,
               "endTime":1696730723,
               "solveCount":1,
               "taskId":74708110322
            }

            >>> await BoundingBoxCaptcha(rucaptcha_key="some_username:some_password",
            ...             service_type="deathbycaptcha"
            ...             ).aio_captcha_handler(captcha_link="https://rucaptcha.com/dist/web/99581b9d446a509a0a01954438a5e36a.jpg")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "bounding_boxes": [
                        {
                            "xMin": 310,
                            "xMax": 385,
                            "yMin": 231,
                            "yMax": 308
                        }
                    ]
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
            >>> await BoundingBoxCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122"
            ...             ).aio_captcha_handler(captcha_base64=file_data)
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "bounding_boxes": [
                        {
                            "xMin": 310,
                            "xMax": 385,
                            "yMin": 231,
                            "yMax": 308
                        }
                    ]
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
            https://2captcha.com/api-docs/bounding-box

            https://rucaptcha.com/api-docs/bounding-box
        """
        super().__init__(method=BoundingBoxCaptchaEnm.BoundingBoxTask.value, *args, **kwargs)

        self.save_format = save_format
        self.img_clearing = img_clearing
        self.img_path = img_path

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
        self._body_file_processing(
            save_format=self.save_format,
            file_path=self.img_path,
            captcha_link=captcha_link,
            captcha_file=captcha_file,
            captcha_base64=captcha_base64,
            **kwargs,
        )
        logging.warning(f"{self.result = }")
        logging.warning(f"{self.create_task_payload = }")
        if not self.result.errorId:
            return self._processing_response(**kwargs)
        return self.result.to_dict()

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
        await self._aio_body_file_processing(
            save_format=self.save_format,
            file_path=self.img_path,
            captcha_link=captcha_link,
            captcha_file=captcha_file,
            captcha_base64=captcha_base64,
            **kwargs,
        )
        if not self.result.errorId:
            return await self._aio_processing_response()
        return self.result.to_dict()

    def __del__(self):
        if self.save_format == SaveFormatsEnm.CONST.value and self.img_clearing:
            shutil.rmtree(self.img_path)
