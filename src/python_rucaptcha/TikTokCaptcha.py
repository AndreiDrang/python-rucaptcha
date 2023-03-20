from .core.base import BaseCaptcha
from .core.enums import TikTokCaptchaEnm


class TikTokCaptcha(BaseCaptcha):
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
        """
        The class is used to work with TikTokCaptcha.
        Solve description:
            https://rucaptcha.com/api-rucaptcha#solving_tiktok
        """
        raise DeprecationWarning("This method is temporarily not supported.".upper())
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

    async def aio_captcha_handler(self):
        """
        The method is responsible for sending data to the server to solve the captcha
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        return await self._aio_processing_response()
