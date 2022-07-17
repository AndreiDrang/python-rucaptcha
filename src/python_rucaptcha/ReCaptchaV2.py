from .base import BaseCaptcha
from .enums import ReCaptcha


class BaseReCaptchaV2(BaseCaptcha):
    def __init__(self, pageurl: str, googlekey: str, method: str = ReCaptcha.USER_RECAPTCHA.value, *args, **kwargs):
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"googlekey": googlekey, "pageurl": pageurl})

        # check user params
        if method not in ReCaptcha.list_values():
            raise ValueError(f"Invalid method parameter set, available - {ReCaptcha.list_values()}")


class ReCaptchaV2(BaseReCaptchaV2):
    """
    The class is used to work with ReCaptchaV2.
    Capy is a captcha in the form of a puzzle
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_recaptchav2_new
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


class aioReCaptchaV2(BaseReCaptchaV2):
    """
    Class for async solve ReCaptchaV2 captcha
    Capy is a captcha in the form of a puzzle
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_recaptchav2_new
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
