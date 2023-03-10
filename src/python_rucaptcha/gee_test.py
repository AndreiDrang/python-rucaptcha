from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import GeetestEnm

from typing import Optional
class GeeTest(BaseCaptcha):
    def __init__(
        self,
        pageurl: str,
        method: str,
        gt: str = None,
        captcha_id: str = None,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Arkose Labs FunCaptcha.

        Args:
            rucaptcha_key: User API key
            pageurl: Full URL of the captcha page
            publickey: The value of the `pk` or `data-pkey` parameter you found in the page code
            method: Captcha type

        Examples:
            >>> FunCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://api.funcaptcha.com/tile-game-lite-mode/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC&lang=en",
            ...             publickey="69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
            ...             surl="https://client-api.arkoselabs.com",
            ...             method=FunCaptchaEnm.FUNCAPTCHA.value
            ...             ).captcha_handler()
            {
               "serverAnswer":{},
               "captchaSolve": "23217....ger",
               "taskId": "73045070203",
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_geetest
            https://rucaptcha.com/api-rucaptcha#geetest-v4
        """
        self.method = method
        super().__init__(method=self.method, *args, **kwargs)
        # check user params
        if self.method not in GeetestEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {GeetestEnm.list_values()}")

        # insert `gt` param to payload
        self.post_payload.update({"gt": gt, "pageurl": pageurl, "captcha_id": captcha_id})

        if self.method == GeetestEnm.GEETEST_V4.value and captcha_id is None:
            raise ValueError(f"For {self.method} captcha_id is required")
        elif self.method == GeetestEnm.GEETEST.value and gt is None:
            raise ValueError(f"For {self.method} gt is required")

    def captcha_handler(self, challenge: Optional[str] = None, **kwargs) -> dict:
        """
        Sync solving method

        :param challenge: The value of the challenge parameter found on the site
        :param kwargs: Parameters for the `requests` library
        """
        if self.method == GeetestEnm.GEETEST.value:
            if challenge is not None:
                self.post_payload.update({"challenge": challenge})
            else:
                raise ValueError(f"For {self.method} challenge is required")

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self, challenge: Optional[str] = None) -> dict:
        """
        Async solving method

        :param challenge: The value of the challenge parameter found on the site
        """
        if self.method == GeetestEnm.GEETEST.value:
            if challenge is not None:
                self.post_payload.update({"challenge": challenge})
            else:
                raise ValueError(f"For {self.method} challenge is required")

        return await self._aio_processing_response()
