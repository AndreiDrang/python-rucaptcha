from .base import BaseCaptcha
from .enums import TurnstileCaptchaEnm


class BaseTurnstile(BaseCaptcha):
    def __init__(
        self, pageurl: str, sitekey: str, method: str = TurnstileCaptchaEnm.TURNSTILE.value, *args, **kwargs
    ):
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"sitekey": sitekey, "pageurl": pageurl})

        # check user params
        if method not in TurnstileCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {TurnstileCaptchaEnm.list_values()}")


class Turnstile(BaseTurnstile):
    """
    The class is used to work with Cloudflare Turnstile
    Solve description:
        https://rucaptcha.com/api-rucaptcha#turnstile
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


class aioTurnstile(BaseTurnstile):
    """
    The class is used to work with Cloudflare Turnstile
    Solve description:
        https://rucaptcha.com/api-rucaptcha#turnstile
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
