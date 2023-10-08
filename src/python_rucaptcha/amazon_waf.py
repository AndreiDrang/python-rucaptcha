from .core.base import BaseCaptcha
from .core.enums import AmazonWAFCaptchaEnm


class AmazonWAF(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        iv: str,
        context: str,
        method: str = AmazonWAFCaptchaEnm.AmazonTaskProxyless.value,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Amazon WAF

        Args:
            rucaptcha_key: User API key
            pageurl: Full URL of the captcha page
            sitekey: Key value from the page
            iv: Value iv from the page
            context: Value of context from page
            method: Captcha type

        Examples:
            >>> AmazonWAF(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...           pageurl="https://page-with-waf.com/",
            ...           sitekey="some-site-key",
            ...           iv="some-iv-value",
            ...           context="some-context-value").captcha_handler()
            {
                'captchaSolve': 'eyJ0e......jNuSFqtyP4Ho',
                'taskId': '7111111984',
                'error': False,
                'errorBody': None
            }

            >>> AmazonWAF(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...           pageurl="https://page-with-waf.com/",
            ...           sitekey="some-site-key",
            ...           iv="some-iv-value",
            ...           context="some-context-value").aio_captcha_handler()
            {
                'captchaSolve': 'eyJ0e......jNuSFqtyP4Ho',
                'taskId': '7111111984',
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#amazon-waf
        """
        super().__init__(method=method, *args, **kwargs)

        # check user params
        if method not in AmazonWAFCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {AmazonWAFCaptchaEnm.list_values()}")

    def captcha_handler(self, **kwargs) -> dict:
        """
        Synchronous method for captcha solving

        Examples:
            >>> AmazonWAF(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...           pageurl="https://page-with-waf.com/",
            ...           sitekey="some-site-key",
            ...           iv="some-iv-value",
            ...           context="some-context-value").captcha_handler()
            {
                'captchaSolve': 'eyJ0e......jNuSFqtyP4Ho',
                'taskId': '7111111984',
                'error': False,
                'errorBody': None
            }

        Returns:
            Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name

        Notes:
            Check class docstirng for more info
        """

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self) -> dict:
        """
        Asynchronous method for captcha solving

        Examples:
            >>> await AmazonWAF(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...           pageurl="https://page-with-waf.com/",
            ...           sitekey="some-site-key",
            ...           iv="some-iv-value",
            ...           context="some-context-value").aio_captcha_handler()
            {
                'captchaSolve': 'eyJ0e......jNuSFqtyP4Ho',
                'taskId': '7111111984',
                'error': False,
                'errorBody': None
            }

        Returns:
            Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name

        Notes:
            Check class docstirng for more info
        """
        return await self._aio_processing_response()
