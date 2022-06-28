from .base import BaseCaptcha
from .enums import GeetestEnm


class BaseGeeTest(BaseCaptcha):
    def __init__(self, pageurl: str, gt: str = None, captcha_id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # insert `gt` param to payload
        self.post_payload.update({"gt": gt, "pageurl": pageurl, "captcha_id": captcha_id})

        # check user params
        assert self.method in GeetestEnm.list_values()
        if self.method == GeetestEnm.GEETEST_V4.value:
            assert captcha_id is not None
        elif self.method == GeetestEnm.GEETEST.value:
            assert gt is not None


class GeeTest(BaseGeeTest):
    """
    Class for solve Geetest and Geetest v4 captcha
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_geetest
        https://rucaptcha.com/api-rucaptcha#geetest-v4
    """

    def captcha_handler(self, challenge: str = None, **kwargs):
        """
        The method is responsible for sending data to the server to solve the captcha
        :param challenge: The value of the challenge parameter found on the site
        :param kwargs: Parameters for the `requests` library
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the Id of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        if self.method == GeetestEnm.GEETEST.value:
            assert challenge is not None
            self.post_payload.update({"challenge": challenge})
        return self._processing_response(**kwargs)


class aioGeeTest(BaseGeeTest):
    """
    Class for async solve Geetest and Geetest v4 captcha
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_geetest
        https://rucaptcha.com/api-rucaptcha#geetest-v4
    """

    async def captcha_handler(self, challenge: str = None):
        """
        The method is responsible for sending data to the server to solve the captcha
        :param challenge: The value of the challenge parameter found on the site
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the Id of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        if self.method == GeetestEnm.GEETEST.value:
            assert challenge is not None
            self.post_payload.update({"challenge": challenge})
        return await self._aio_processing_response()
