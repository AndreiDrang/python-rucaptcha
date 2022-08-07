from .base import BaseCaptcha
from .enums import GeetestEnm


class BaseGeeTest(BaseCaptcha):
    def __init__(
        self,
        pageurl: str,
        method: str,
        gt: str = None,
        captcha_id: str = None,
        *args,
        **kwargs,
    ):
        self.method = method
        # check user params
        if self.method not in GeetestEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {GeetestEnm.list_values()}")

        super().__init__(method=self.method, *args, **kwargs)
        # insert `gt` param to payload
        self.post_payload.update({"gt": gt, "pageurl": pageurl, "captcha_id": captcha_id})

        if self.method == GeetestEnm.GEETEST_V4.value and captcha_id is None:
            raise ValueError(f"For {self.method} captcha_id is required")
        elif self.method == GeetestEnm.GEETEST.value and gt is None:
            raise ValueError(f"For {self.method} gt is required")


class GeeTest(BaseGeeTest):
    """
    Class for solve Geetest and Geetest v4 captcha
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_geetest
        https://rucaptcha.com/api-rucaptcha#geetest-v4
    """

    def captcha_handler(self, challenge: str = None, **kwargs) -> dict:
        """
        The method is responsible for sending data to the server to solve the captcha
        :param challenge: The value of the challenge parameter found on the site
        :param kwargs: Parameters for the `requests` library
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        if self.method == GeetestEnm.GEETEST.value:
            if challenge is not None:
                self.post_payload.update({"challenge": challenge})
            else:
                raise ValueError(f"For {self.method} challenge is required")

        return self._processing_response(**kwargs)


class aioGeeTest(BaseGeeTest):
    """
    Class for async solve Geetest and Geetest v4 captcha
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_geetest
        https://rucaptcha.com/api-rucaptcha#geetest-v4
    """

    async def captcha_handler(self, challenge: str = None) -> dict:
        """
        The method is responsible for sending data to the server to solve the captcha
        :param challenge: The value of the challenge parameter found on the site
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        if self.method == GeetestEnm.GEETEST.value:
            if challenge is not None:
                self.post_payload.update({"challenge": challenge})
            else:
                raise ValueError(f"For {self.method} challenge is required")

        return await self._aio_processing_response()
