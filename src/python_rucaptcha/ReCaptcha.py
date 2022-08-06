from .base import BaseCaptcha
from .enums import ReCaptchaEnm


class BaseReCaptcha(BaseCaptcha):
    def __init__(self, pageurl: str, googlekey: str, method: str = ReCaptchaEnm.USER_RECAPTCHA.value, *args, **kwargs):
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"googlekey": googlekey, "pageurl": pageurl})

        # check user params
        if method not in ReCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {ReCaptchaEnm.list_values()}")


class ReCaptcha(BaseReCaptcha):
    """
    The class is used to work with ReCaptcha
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_recaptchav2_new
        https://rucaptcha.com/api-rucaptcha#invisible
        https://rucaptcha.com/api-rucaptcha#solving_recaptchav3
        https://rucaptcha.com/api-rucaptcha#solving_recaptcha_enterprise
    """

    def captcha_handler(self, **kwargs):
        """
        The method is responsible for sending data to the server to solve the captcha
        :param kwargs: Parameters for the `requests` library
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the Id of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """

        return self._processing_response(**kwargs)


class aioReCaptcha(BaseReCaptcha):
    """
    The class is used to async work with ReCaptcha
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_recaptchav2_new
        https://rucaptcha.com/api-rucaptcha#invisible
        https://rucaptcha.com/api-rucaptcha#solving_recaptchav3
        https://rucaptcha.com/api-rucaptcha#solving_recaptcha_enterprise
    """

    async def captcha_handler(self):
        """
        The method is responsible for sending data to the server to solve the captcha
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the Id of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        return await self._aio_processing_response()
