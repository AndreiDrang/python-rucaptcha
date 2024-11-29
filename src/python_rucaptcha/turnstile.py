from typing import Union

from .core.base import BaseCaptcha
from .core.enums import TurnstileCaptchaEnm


class Turnstile(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        userAgent: str,
        method: Union[str, TurnstileCaptchaEnm] = TurnstileCaptchaEnm.TurnstileTaskProxyless,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Cloudflare Turnstile.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            websiteKey: The value of the `sitekey` parameter found on the site
            userAgent: Your browser UserAgent
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> Turnstile(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://www.geetest.com/en/demo",
            ...             websiteKey="0x4AAAAAAAC3DHQFLr1GavRN",
            ...             method=TurnstileCaptchaEnm.TurnstileTaskProxyless.value,
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"0.zrSnRHO7h0HwSjSCU8oyzbjEtD8p.d62306d4ee00c77dda697f959ebbd7bd97",
                  "userAgent":"Mozilla/5.0 (....."
               },
               "cost":"0.00145",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

            >>> await Turnstile(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://www.geetest.com/en/demo",
            ...             websiteKey="0x4AAAAAAAC3DHQFLr1GavRN",
            ...             method=TurnstileCaptchaEnm.TurnstileTaskProxyless.value,
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"0.zrSnRHO7h0HwSjSCU8oyzbjEtD8p.d62306d4ee00c77dda697f959ebbd7bd97",
                  "userAgent":"Mozilla/5.0 (....."
               },
               "cost":"0.00145",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-docs/cloudflare-turnstile
        """

        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update(
            {"websiteURL": websiteURL, "websiteKey": websiteKey, "userAgent": userAgent}
        )

        # check user params
        if method not in TurnstileCaptchaEnm.list_values():
            raise ValueError(
                f"Invalid method parameter set, available - {TurnstileCaptchaEnm.list_values()}")

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
