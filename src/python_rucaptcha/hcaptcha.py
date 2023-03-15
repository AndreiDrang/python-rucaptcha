from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import HCaptchaEnm


class HCaptcha(BaseCaptcha):

    def __init__(
        self,
        sitekey: str,
        pageurl: str,
        method: str = HCaptchaEnm.HCAPTCHA.value,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with HCaptcha.

        Args:
            rucaptcha_key: User API key
            sitekey: The value of the `data-sitekey` parameter found on the site
            pageurl: Full URL of the captcha page
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> HCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             sitekey="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             pageurl="https://rucaptcha.com/demo/hcaptcha",
            ...             method=HCaptchaEnm.HCAPTCHA.value
            ...             ).captcha_handler()
            {
               "captchaSolve": "P1_eyJ.....cp_J",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

            >>> await HCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             sitekey="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             pageurl="https://rucaptcha.com/demo/hcaptcha",
            ...             method=HCaptchaEnm.HCAPTCHA.value
            ...             ).aio_captcha_handler()
            {
               "captchaSolve": "P1_eyJ.....cp_J",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_hcaptcha
        """
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"pageurl": pageurl, "sitekey": sitekey})

        # check user params
        if method not in HCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {HCaptchaEnm.list_values()}")

    def captcha_handler(self, **kwargs):
        """
        Sync solving method

        Args:
            kwargs: Parameters for the `requests` library

        Examples:
            >>> HCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             sitekey="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             pageurl="https://rucaptcha.com/demo/hcaptcha",
            ...             method=HCaptchaEnm.HCAPTCHA.value
            ...             ).captcha_handler()
            {
               "captchaSolve": "P1_eyJ.....cp_J",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self):
        """
        Async solving method

        Examples:
            >>> await HCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             sitekey="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             pageurl="https://rucaptcha.com/demo/hcaptcha",
            ...             method=HCaptchaEnm.HCAPTCHA.value
            ...             ).aio_captcha_handler()
            {
               "captchaSolve": "P1_eyJ.....cp_J",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        return await self._aio_processing_response()
