from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import YandexSmartCaptchaEnm


class BaseYandexSmartCaptcha(BaseCaptcha):
    def __init__(self, pageurl: str, sitekey: str, method: str = YandexSmartCaptchaEnm.YANDEX.value, *args, **kwargs):
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"sitekey": sitekey, "pageurl": pageurl})

        # check user params
        if method not in YandexSmartCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {YandexSmartCaptchaEnm.list_values()}")


class YandexSmartCaptcha(BaseYandexSmartCaptcha):
    """
    The class is used to work with YandexSmart
    Solve description:
        https://rucaptcha.com/api-rucaptcha#yandex
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


class aioYandexSmartCaptcha(BaseYandexSmartCaptcha):
    """
    The class is used to work with YandexSmart
    Solve description:
        https://rucaptcha.com/api-rucaptcha#yandex
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
