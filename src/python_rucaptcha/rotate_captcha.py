import logging
from typing import Optional

from .core.base import BaseCaptcha
from .core.enums import RotateCaptchaEnm


class RotateCaptcha(BaseCaptcha):
    def __init__(self, method: str = RotateCaptchaEnm.RotateTask.value, *args, **kwargs):
        """
        The class is used to work with Rotate Captcha.

        Args:
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> RotateCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).captcha_handler(captcha_file="examples/rotate/rotate_ex.png")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "rotate":180
               },
               "cost":"0.0005",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73043008354
            }

            >>> with open("src/examples/rotate/rotate_ex.png", "rb") as f:
            ...     file_data = f.read()
            >>> RotateCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122"
            ...             ).captcha_handler(captcha_base64=file_data)
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "rotate":180
               },
               "cost":"0.0005",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73043008354
            }

            >>> await RotateCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).aio_captcha_handler(captcha_file="examples/rotate/rotate_ex.png")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "rotate":180
               },
               "cost":"0.0005",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73043008354
            }

            >>> await RotateCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                     angle=45).aio_captcha_handler(captcha_file="examples/rotate/rotate_ex.png")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "rotate":90
               },
               "cost":"0.0005",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73043008354
            }

            >>> with open("src/examples/rotate/rotate_ex.png", "rb") as f:
            ...     file_data = f.read()
            >>> await RotateCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122"
            ...             ).aio_captcha_handler(captcha_base64=file_data)
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "rotate":180
               },
               "cost":"0.0005",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73043008354
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-docs/rotate
        """
        super().__init__(method=method, *args, **kwargs)

        # check user params
        if method not in RotateCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {RotateCaptchaEnm.list_values()}")

    def captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        **kwargs,
    ):
        """
        Async solving method

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
            captcha_link=captcha_link, captcha_file=captcha_file, captcha_base64=captcha_base64, **kwargs
        )
        if not self.result.errorId:
            return self._processing_response(**kwargs)
        return self.result.to_dict()

    async def aio_captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        **kwargs,
    ):
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
            captcha_link=captcha_link, captcha_file=captcha_file, captcha_base64=captcha_base64, **kwargs
        )
        if not self.result.errorId:
            return await self._aio_processing_response()
        return self.result.to_dict()
