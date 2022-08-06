from .base import BaseCaptcha
from .enums import TikTokCaptchaEnm


class BaseTikTokCaptcha(BaseCaptcha):
    def __init__(
        self,
        pageurl: str,
        cookies: str,
        aid: str,
        host: str,
        method: str = TikTokCaptchaEnm.TIKTOK.value,
        *args,
        **kwargs,
    ):
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update(
            {
                "pageurl": pageurl,
                "cookies": cookies,
                "aid": aid,
                "host": host,
            }
        )

        # check user params
        if method not in TikTokCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {TikTokCaptchaEnm.list_values()}")


class TikTokCaptcha(BaseTikTokCaptcha):
    """
    The class is used to work with TikTokCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_tiktok
    """

    def captcha_handler(self, **kwargs):
        """
        The method is responsible for sending data to the server to solve the captcha
        :param kwargs: Parameters for the `requests` library
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """

        return self._processing_response(**kwargs)


class aioTikTokCaptcha(BaseTikTokCaptcha):
    """
    The class is used to async work with TikTokCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_tiktok
    """

    async def captcha_handler(self):
        """
        The method is responsible for sending data to the server to solve the captcha
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        return await self._aio_processing_response()
