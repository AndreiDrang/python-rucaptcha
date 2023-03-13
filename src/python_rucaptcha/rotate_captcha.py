import base64
from typing import Optional

from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import RotateCaptchaEnm


class RotateCaptcha(BaseCaptcha):
    """
    The class is used to work with RotateCaptcha
    Solve description:
    """

    def __init__(self, method: str = RotateCaptchaEnm.ROTATECAPTCHA.value, *args, **kwargs):
        """
        The class is used to work with Rotate Captcha.

        Args:
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> RotateCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).captcha_handler(captcha_file="examples/rotate/rotate_ex.png")
            {
                'captchaSolve': '160',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

            >>> await RotateCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             ).aio_captcha_handler(captcha_file="examples/rotate/rotate_ex.png")
            {
                'captchaSolve': '160',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

            >>> await RotateCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                     angle=45).aio_captcha_handler(captcha_file="examples/rotate/rotate_ex.png")
            {
                'captchaSolve': '125',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_rotatecaptcha
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

        Examples:
            >>> RotateCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                 angle=45).captcha_handler(captcha_file="examples/rotate/rotate_ex.png")
            {
                'captchaSolve': '125',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_funcaptcha_new
        """

        # if a local file link is passed
        if captcha_file:
            self.post_payload.update(
                {"body": base64.b64encode(self._local_image_captcha(captcha_file)).decode("utf-8")}
            )
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.post_payload.update({"body": base64.b64encode(captcha_base64).decode("utf-8")})
        # if a URL is passed
        elif captcha_link:
            try:
                content = self.url_open(url=captcha_link, **kwargs).content
                self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})
            except Exception as error:
                self.result.error = True
                self.result.errorBody = str(error)
                return self.result.dict()

        else:
            # if none of the parameters are passed
            self.result.error = True
            self.result.errorBody = self.NO_CAPTCHA_ERR
            return self.result.dict()
        return self._processing_response(**kwargs)

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

        Examples:
            >>> await RotateCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                     angle=45).aio_captcha_handler(captcha_file="examples/rotate/rotate_ex.png")
            {
                'captchaSolve': '125',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_funcaptcha_new
        """

        # if a local file link is passed
        if captcha_file:
            self.post_payload.update(
                {"body": base64.b64encode(self._local_image_captcha(captcha_file)).decode("utf-8")}
            )
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.post_payload.update({"body": base64.b64encode(captcha_base64).decode("utf-8")})
        # if a URL is passed
        elif captcha_link:
            try:
                content = await self.aio_url_read(url=captcha_link, **kwargs)
                self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})
            except Exception as error:
                self.result.error = True
                self.result.errorBody = str(error)
                return self.result.dict()

        else:
            # if none of the parameters are passed
            self.result.error = True
            self.result.errorBody = self.NO_CAPTCHA_ERR
            return self.result.dict()

        return await self._aio_processing_response()
