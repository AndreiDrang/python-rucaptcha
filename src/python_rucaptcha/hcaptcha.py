from typing import Union

from .core.base import BaseCaptcha
from .core.enums import HCaptchaEnm


class HCaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        method: Union[str, HCaptchaEnm] = HCaptchaEnm.HCaptchaTaskProxyless,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with HCaptcha.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            websiteKey: The value of the `data-sitekey` parameter found on the site
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> HCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteKey="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             websiteURL="https://rucaptcha.com/demo/hcaptcha",
            ...             method=HCaptchaEnm.HCaptchaTaskProxyless.value
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"P1_eyJ0eXAiOiJKV...1LDq89KyJ5A",
                  "respKey":"E0_eyJ0eXAiOiJK...y2w5_YbP8PGuJBBo",
                  "userAgent":"Mozilla/5.0 (.......",
                  "gRecaptchaResponse":"P1_eyJ0eXAiOiJKV...1LDq89KyJ5A"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

            >>> await HCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteKey="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             websiteURL="https://rucaptcha.com/demo/hcaptcha",
            ...             method=HCaptchaEnm.HCaptchaTaskProxyless.value
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"P1_eyJ0eXAiOiJKV...1LDq89KyJ5A",
                  "respKey":"E0_eyJ0eXAiOiJK...y2w5_YbP8PGuJBBo",
                  "userAgent":"Mozilla/5.0 (........",
                  "gRecaptchaResponse":"P1_eyJ0eXAiOiJKV...1LDq89KyJ5A"
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
            https://rucaptcha.com/api-docs/hcaptcha
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update({"websiteURL": websiteURL, "websiteKey": websiteKey})

        # check user params
        if method not in HCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {HCaptchaEnm.list_values()}")

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
