from .base import BaseCaptcha
from .enums import LeminCroppedCaptchaEnm


class BaseLeminCroppedCaptcha(BaseCaptcha):
    def __init__(
        self,
        pageurl: str,
        captcha_id: str,
        div_id: str,
        method: str = LeminCroppedCaptchaEnm.LEMIN.value,
        *args,
        **kwargs,
    ):
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"pageurl": pageurl, "captcha_id": captcha_id, "div_id": div_id})

        # check user params
        if method not in LeminCroppedCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {LeminCroppedCaptchaEnm.list_values()}")


class LeminCroppedCaptcha(BaseLeminCroppedCaptcha):
    """
    The class is used to work with LeminCroppedCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#lemin
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


class aioLeminCroppedCaptcha(BaseLeminCroppedCaptcha):
    """
    Class for async solve LeminCroppedCaptcha captcha
    Solve description:
        https://rucaptcha.com/api-rucaptcha#lemin
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
