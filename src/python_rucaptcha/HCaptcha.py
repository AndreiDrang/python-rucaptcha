from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import HCaptchaEnm


class BaseHCaptcha(BaseCaptcha):
    def __init__(
        self,
        sitekey: str,
        pageurl: str,
        method: str = HCaptchaEnm.HCAPTCHA.value,
        *args,
        **kwargs,
    ):
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"pageurl": pageurl, "sitekey": sitekey})

        # check user params
        if method not in HCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {HCaptchaEnm.list_values()}")


class HCaptcha(BaseHCaptcha):
    """
    The class is used to work with HCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_hcaptcha
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


class aioHCaptcha(BaseHCaptcha):
    """
    The class is used to async work with HCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_hcaptcha
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
