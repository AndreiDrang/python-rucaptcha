from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import LeminCroppedCaptchaEnm


class LeminCroppedCaptcha(BaseCaptcha):
    def __init__(
        self,
        pageurl: str,
        captcha_id: str,
        div_id: str,
        method: str = LeminCroppedCaptchaEnm.LEMIN.value,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Lemin Cropped Captcha.

        Args:
            rucaptcha_key: User API key
            pageurl: Full URL of the captcha page
            captcha_id: The value of the `captcha_id` parameter found on the site
            div_id: The `id` of the parent `div`, which contains the captcha
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> LeminCroppedCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                     pageurl="https://dashboard.leminnow.com/auth/signup",
            ...                     captcha_id="CROPPED_099216d_8ba061383fa24ef498115023aa7189d4",
            ...                     div_id="lemin-cropped-captcha",
            ...                     method=LeminCroppedCaptchaEnm.LEMIN.value,
            ...                     api_server="api.leminnow.com"
            ...                     ).captcha_handler()
            {
               "captchaSolve": {
                  "answer":"0xc....EUa",
                  "challenge_id":"58.....63a"
               },
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

            >>> await LeminCroppedCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                     pageurl="https://dashboard.leminnow.com/auth/signup",
            ...                     captcha_id="CROPPED_099216d_8ba061383fa24ef498115023aa7189d4",
            ...                     div_id="lemin-cropped-captcha",
            ...                     method=LeminCroppedCaptchaEnm.LEMIN.value,
            ...                     api_server="api.leminnow.com"
            ...                     ).aio_captcha_handler()
            {
               "captchaSolve": {
                  "answer":"0xc....EUa",
                  "challenge_id":"58.....63a"
               },
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#lemin
        """
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"pageurl": pageurl, "captcha_id": captcha_id, "div_id": div_id})

        # check user params
        if method not in LeminCroppedCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {LeminCroppedCaptchaEnm.list_values()}")

    def captcha_handler(self, **kwargs):
        """
        Sync solving method

        Args:
            kwargs: Parameters for the `requests` library

        Examples:
            >>> LeminCroppedCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                     pageurl="https://dashboard.leminnow.com/auth/signup",
            ...                     captcha_id="CROPPED_099216d_8ba061383fa24ef498115023aa7189d4",
            ...                     div_id="lemin-cropped-captcha",
            ...                     method=LeminCroppedCaptchaEnm.LEMIN.value,
            ...                     api_server="api.leminnow.com"
            ...                     ).captcha_handler()
            {
               "captchaSolve": {
                  "answer":"0xc....EUa",
                  "challenge_id":"58.....63a"
               },
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#lemin
        """
        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self):
        """
        Async solving method

        Examples:
            >>> LeminCroppedCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                     pageurl="https://dashboard.leminnow.com/auth/signup",
            ...                     captcha_id="CROPPED_099216d_8ba061383fa24ef498115023aa7189d4",
            ...                     div_id="lemin-cropped-captcha",
            ...                     method=LeminCroppedCaptchaEnm.LEMIN.value,
            ...                     api_server="api.leminnow.com"
            ...                     ).captcha_handler()
            {
               "captchaSolve": {
                  "answer":"0xc....EUa",
                  "challenge_id":"58.....63a"
               },
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#lemin
        """
        return await self._aio_processing_response()
