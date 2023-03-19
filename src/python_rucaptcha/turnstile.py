from .core.base import BaseCaptcha
from .core.enums import TurnstileCaptchaEnm


class Turnstile(BaseCaptcha):
    def __init__(self, pageurl: str, sitekey: str, method: str = TurnstileCaptchaEnm.TURNSTILE.value, *args, **kwargs):
        """
        The class is used to work with Cloudflare Turnstile.

        Args:
            rucaptcha_key: User API key
            pageurl: Full URL of the captcha page
            sitekey: The value of the `sitekey` parameter found on the site
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> Turnstile(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://www.geetest.com/en/demo",
            ...             sitekey="0x4AAAAAAAC3DHQFLr1GavRN",
            ...             method=TurnstileCaptchaEnm.TURNSTILE.value,
            ...             ).captcha_handler()
            {
               "captchaSolve": "0._VMG....Pv",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

            >>> await Turnstile(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://www.geetest.com/en/demo",
            ...             sitekey="0x4AAAAAAAC3DHQFLr1GavRN",
            ...             method=TurnstileCaptchaEnm.TURNSTILE.value,
            ...             ).aio_captcha_handler()
            {
               "captchaSolve": "0._VMG....Pv",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#turnstile
        """
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"sitekey": sitekey, "pageurl": pageurl})

        # check user params
        if method not in TurnstileCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {TurnstileCaptchaEnm.list_values()}")

    def captcha_handler(self, **kwargs):
        """
        Sync solving method

        Args:
            kwargs: Parameters for the `requests` library

        Examples:
            >>> Turnstile(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://www.geetest.com/en/demo",
            ...             sitekey="0x4AAAAAAAC3DHQFLr1GavRN",
            ...             method=TurnstileCaptchaEnm.TURNSTILE.value,
            ...             ).captcha_handler()
            {
               "captchaSolve": "0._VMG....Pv",
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
            >>> await Turnstile(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://www.geetest.com/en/demo",
            ...             sitekey="0x4AAAAAAAC3DHQFLr1GavRN",
            ...             method=TurnstileCaptchaEnm.TURNSTILE.value,
            ...             ).aio_captcha_handler()
            {
               "captchaSolve": "0._VMG....Pv",
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
