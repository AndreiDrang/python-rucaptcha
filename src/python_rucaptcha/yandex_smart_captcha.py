from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import YandexSmartCaptchaEnm


class YandexSmartCaptcha(BaseCaptcha):
    def __init__(self, pageurl: str, sitekey: str, method: str = YandexSmartCaptchaEnm.YANDEX.value, *args, **kwargs):
        """
        The class is used to work with Yandex Smart Captcha

        Args:
            rucaptcha_key: User API key
            pageurl: Full URL of the captcha page
            sitekey: The value of the `data-sitekey` parameter found on the site
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> YandexSmartCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://captcha-api.yandex.ru/demo",
            ...             sitekey="FEXfAbHQsToo97VidNVk3j4dC74nGW1DgdxjtNB9",
            ...             method=YandexSmartCaptchaEnm.YANDEX.value,
            ...             ).captcha_handler()
            {
               "captchaSolve": "dD0x....Pv",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

            >>> YandexSmartCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://captcha-api.yandex.ru/demo",
            ...             sitekey="FEXfAbHQsToo97VidNVk3j4dC74nGW1DgdxjtNB9"
            ...             ).captcha_handler()
            {
               "captchaSolve": "dD0x....Pv",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

            >>> await YandexSmartCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://captcha-api.yandex.ru/demo",
            ...             sitekey="FEXfAbHQsToo97VidNVk3j4dC74nGW1DgdxjtNB9",
            ...             method=YandexSmartCaptchaEnm.YANDEX.value,
            ...             ).aio_captcha_handler()
            {
               "captchaSolve": "dD0x....Pv",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

            >>> await YandexSmartCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://captcha-api.yandex.ru/demo",
            ...             sitekey="FEXfAbHQsToo97VidNVk3j4dC74nGW1DgdxjtNB9"
            ...             ).aio_captcha_handler()
            {
               "captchaSolve": "dD0x....Pv",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#yandex
        """
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"sitekey": sitekey, "pageurl": pageurl})

        # check user params
        if method not in YandexSmartCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {YandexSmartCaptchaEnm.list_values()}")

    def captcha_handler(self, **kwargs):
        """
        Sync solving method

        Args:
            kwargs: Parameters for the `requests` library

        Examples:
            >>> YandexSmartCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://captcha-api.yandex.ru/demo",
            ...             sitekey="FEXfAbHQsToo97VidNVk3j4dC74nGW1DgdxjtNB9"
            ...             ).captcha_handler()
            {
               "captchaSolve": "dD0x....Pv",
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
            >>> await YandexSmartCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://captcha-api.yandex.ru/demo",
            ...             sitekey="FEXfAbHQsToo97VidNVk3j4dC74nGW1DgdxjtNB9"
            ...             ).aio_captcha_handler()
            {
               "captchaSolve": "dD0x....Pv",
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
