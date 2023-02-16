import base64

import aiohttp

from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import RotateCaptchaEnm


class BaseRotateCaptcha(BaseCaptcha):
    def __init__(self, method: str = RotateCaptchaEnm.ROTATECAPTCHA.value, *args, **kwargs):
        super().__init__(method=method, *args, **kwargs)

        # check user params
        if method not in RotateCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {RotateCaptchaEnm.list_values()}")


class RotateCaptcha(BaseRotateCaptcha):
    """
    The class is used to work with RotateCaptcha
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_rotatecaptcha
    """

    def captcha_handler(self, captcha_link: str, **kwargs):
        """
        The method is responsible for sending data to the server to solve the captcha
        :param captcha_link: link or path to captcha file
        :param kwargs: Parameters for the `requests` library
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        # if user send link - download file
        if "http" in captcha_link:
            content: bytes = self.url_open(url=captcha_link, **kwargs).content
        # is user send file path - read ir
        else:
            with open(captcha_link, "rb") as captcha_image:
                content: bytes = captcha_image.read()
        # decode file data in base64 and prepare payload
        self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})

        return self._processing_response(**kwargs)


class aioRotateCaptcha(BaseRotateCaptcha):
    """
    The class is used to async work with RotateCaptcha
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_rotatecaptcha
    """

    async def captcha_handler(self, captcha_link: str, **kwargs):
        """
        The method is responsible for sending data to the server to solve the captcha
        :param captcha_link: link or path to captcha file
        :param kwargs: Parameters for the `requests` library
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        # if user send link - download file
        if "http" in captcha_link:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=captcha_link) as resp:
                    content: bytes = await resp.content.read()
        # if user send file path - read it
        else:
            with open(captcha_link, "rb") as captcha_image:
                content: bytes = captcha_image.read()
        # decode file data in base64 and prepare payload
        self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})

        return await self._aio_processing_response()
