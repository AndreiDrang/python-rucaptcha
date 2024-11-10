from typing import Union

from .core.base import BaseCaptcha
from .core.enums import MTCaptchaEnm


class MTCaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        method: Union[str, MTCaptchaEnm] = MTCaptchaEnm.MtCaptchaTaskProxyless.value,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with HCaptcha.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            websiteKey: The MTCaptcha `sitekey` value found in the page code.
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> MTCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://service.mtcaptcha.com/mtcv1/demo/index.html",
            ...             websiteKey="MTPublic-DemoKey9M",
            ...             method=MTCaptchaEnm.MtCaptchaTaskProxyless,
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "token": "datadome=4ZXwCBlyHx9ktZhSnycMF...; Path=/; Secure; SameSite=Lax"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

            >>> await MTCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://service.mtcaptcha.com/mtcv1/demo/index.html",
            ...             websiteKey="MTPublic-DemoKey9M",
            ...             method=MTCaptchaEnm.MtCaptchaTaskProxyless,
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "token": "datadome=4ZXwCBlyHx9ktZhSnycMF...; Path=/; Secure; SameSite=Lax"
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
            https://2captcha.com/api-docs/mtcaptcha
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update({"websiteURL": websiteURL,
                                                 "websiteKey": websiteKey})
        # check user params
        if method not in MTCaptchaEnm.list_values():
            raise ValueError(
                f"Invalid method parameter set, available - {MTCaptchaEnm.list_values()}")

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
