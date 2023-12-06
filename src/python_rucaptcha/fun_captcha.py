from .core.base import BaseCaptcha
from .core.enums import FunCaptchaEnm


class FunCaptcha(BaseCaptcha):
    def __init__(self, pageurl: str, publickey: str, method: str = FunCaptchaEnm.FUNCAPTCHA.value, *args, **kwargs):
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
               "captchaSolve": "23217....ger",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_funcaptcha_new
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update({"publickey": publickey, "pageurl": pageurl})

        # check user params
        if method not in FunCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {FunCaptchaEnm.list_values()}")

    def captcha_handler(self, **kwargs):
        """
        Sync solving method

        Args:
            kwargs: additional params for `requests` library

        Examples:
            >>> FunCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://api.funcaptcha.com/tile-game-lite-mode/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC&lang=en",
            ...             publickey="69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
            ...             method=FunCaptchaEnm.FUNCAPTCHA.value,
            ...             surl="https://client-api.arkoselabs.com",
            ...             userAgent="some-user-agent"
            ...             ).captcha_handler()
            {
               "captchaSolve": "23217....ger",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
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
            >>> await FunCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://api.funcaptcha.com/tile-game-lite-mode/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC&lang=en",
            ...             publickey="69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
            ...             method=FunCaptchaEnm.FUNCAPTCHA.value,
            ...             surl="https://client-api.arkoselabs.com",
            ...             userAgent="some-user-agent"
            ...             ).aio_captcha_handler()
            {
               "captchaSolve": "23217....ger",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_funcaptcha_new
        """
        return await self._aio_processing_response()
