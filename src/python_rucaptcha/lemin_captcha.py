from typing import Union

from .core.base import BaseCaptcha
from .core.enums import LeminCaptchaEnm


class LeminCaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        captchaId: str,
        div_id: str,
        method: Union[str, LeminCaptchaEnm] = LeminCaptchaEnm.LeminTaskProxyless,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Lemin Cropped Captcha.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            captchaId: The value of the `captcha_id` parameter found on the site
            div_id: The `id` of the parent `div`, which contains the captcha
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> LeminCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                     websiteURL="https://dashboard.leminnow.com/auth/signup",
            ...                     captchaId="CROPPED_099216d_8ba061383fa24ef498115023aa7189d4",
            ...                     div_id="lemin-cropped-captcha",
            ...                     method=LeminCaptchaEnm.LeminTaskProxyless.value,
            ...                     api_server="api.leminnow.com"
            ...                     ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "answer":"0xaxakx0xaxaax0xkxx3ox0x3ox3ox_...gAAAAABk8bgzEFOg9i3Jm",
                  "challenge_id":"e0348984-92ec-23af-1488-446e3a58946c"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

            >>> await LeminCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                     websiteURL="https://dashboard.leminnow.com/auth/signup",
            ...                     captcha_id="CROPPED_099216d_8ba061383fa24ef498115023aa7189d4",
            ...                     div_id="lemin-cropped-captcha",
            ...                     method=LeminCaptchaEnm.LeminTaskProxyless.value,
            ...                     api_server="api.leminnow.com"
            ...                     ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "answer":"0xaxakx0xaxaax0xkxx3ox0x3ox3ox_...gAAAAABk8bgzEFOg9i3Jm",
                  "challenge_id":"e0348984-92ec-23af-1488-446e3a58946c"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-docs/lemin
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update(
            {"websiteURL": websiteURL, "captchaId": captchaId, "div_id": div_id}
        )

        # check user params
        if method not in LeminCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {LeminCaptchaEnm.list_values()}")

    def captcha_handler(self, **kwargs) -> dict:
        """
        Sync solving method

        Args:
            kwargs: Parameters for the `requests` library

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self) -> dict:
        """
        Async solving method

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        return await self._aio_processing_response()
