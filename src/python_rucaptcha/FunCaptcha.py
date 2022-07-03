from .base import BaseCaptcha
from .enums import FunCaptchaEnm


class BaseFunCaptcha(BaseCaptcha):
    def __init__(self, pageurl: str, publickey: str, method: str = FunCaptchaEnm.FUNCAPTCHA.value, *args, **kwargs):
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"publickey": publickey, "pageurl": pageurl})

        # check user params
        if method not in FunCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {FunCaptchaEnm.list_values()}")


class FunCaptcha(BaseFunCaptcha):
    """
    The class is used to work with FunCaptcha.
    Capy is a captcha in the form of a puzzle
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_funcaptcha_new
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


class aioFunCaptcha(BaseFunCaptcha):
    """
    The class is used to work with FunCaptcha.
    Capy is a captcha in the form of a puzzle
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_funcaptcha_new
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
