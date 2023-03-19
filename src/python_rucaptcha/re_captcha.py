from typing import Optional

from .core.base import BaseCaptcha
from .core.enums import ReCaptchaEnm


class ReCaptcha(BaseCaptcha):
    def __init__(
        self,
        pageurl: str,
        googlekey: str,
        version: Optional[str] = None,
        method: str = ReCaptchaEnm.USER_RECAPTCHA.value,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with ReCaptcha

        Args:
            rucaptcha_key: User API key
            pageurl: Full URL of the captcha page
            googlekey: The value of the `googlekey` parameter you found in the page code
            version: `v3` - indicates that this is reCAPTCHA V3
            method: Captcha type

        Examples:
            >>> ReCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://rucaptcha.com/demo/recaptcha-v2",
            ...             googlekey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH",
            ...             method=ReCaptchaEnm.USER_RECAPTCHA.value
            ...             ).captcha_handler()
            {
                'captchaSolve': '03A....8h',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

            >>> ReCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://rucaptcha.com/demo/recaptcha-v2",
            ...             googlekey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH",
            ...             domain="google.com",
            ...             invisible=1,
            ...             ).captcha_handler()
            {
                'captchaSolve': '03A....8h',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

            >>> ReCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://rucaptcha.com/demo/recaptcha-v2",
            ...             googlekey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH",
            ...             version="v3",
            ...             action="verify",
            ...             min_score=0.2,
            ...             ).captcha_handler()
            {
                'captchaSolve': '03A....8h',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

            >>> await ReCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://rucaptcha.com/demo/recaptcha-v2",
            ...             googlekey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH",
            ...             method=ReCaptchaEnm.USER_RECAPTCHA.value
            ...             ).aio_captcha_handler()
            {
                'captchaSolve': '03A....8h',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_recaptchav2_new
            https://rucaptcha.com/api-rucaptcha#invisible
            https://rucaptcha.com/api-rucaptcha#solving_recaptchav3
            https://rucaptcha.com/api-rucaptcha#solving_recaptcha_enterprise
        """
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"googlekey": googlekey, "pageurl": pageurl, "version": version})

        # check user params
        if method not in ReCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {ReCaptchaEnm.list_values()}")

    def captcha_handler(self, **kwargs):
        """
        Sync solving method

        Args:
            kwargs: additional params for `requests` library

        Examples:
            >>> ReCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://rucaptcha.com/demo/recaptcha-v2",
            ...             googlekey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH",
            ...             method=ReCaptchaEnm.USER_RECAPTCHA.value
            ...             ).captcha_handler()
            {
                'captchaSolve': '03A....8h',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_funcaptcha_new
        """
        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self):
        """
        Async solving method

        Examples:
            >>> await ReCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://rucaptcha.com/demo/recaptcha-v2",
            ...             googlekey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH",
            ...             method=ReCaptchaEnm.USER_RECAPTCHA.value
            ...             ).aio_captcha_handler()
            {
                'captchaSolve': '03A....8h',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_funcaptcha_new
        """
        return await self._aio_processing_response()
