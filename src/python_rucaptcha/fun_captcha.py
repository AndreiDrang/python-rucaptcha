from typing import Union

from .core.base import BaseCaptcha
from .core.enums import FunCaptchaEnm


class FunCaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websitePublicKey: str,
        method: Union[str, FunCaptchaEnm] = FunCaptchaEnm.FunCaptchaTaskProxyless,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Arkose Labs FunCaptcha.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            websitePublicKey: The value of the `pk` or `data-pkey` parameter you found in the page code
            method: Captcha type

        Examples:
            >>> FunCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://api.funcaptcha.com/tile-game-lite-mode/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC&lang=en",
            ...             websitePublicKey="69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
            ...             method=FunCaptchaEnm.FunCaptchaTaskProxyless.value
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"142000f.....er"
               },
               "cost":"0.002",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":0,
               "taskId": 73243152973,
            }

            >>> await FunCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://api.funcaptcha.com/tile-game-lite-mode/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC&lang=en",
            ...             websitePublicKey="69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
            ...             method=FunCaptchaEnm.FunCaptchaTaskProxyless.value
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"142000f.....er"
               },
               "cost":"0.002",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":0,
               "taskId": 73243152973,
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-docs/arkoselabs-funcaptcha
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update(
            {"websiteURL": websiteURL, "websitePublicKey": websitePublicKey}
        )

        # check user params
        if method not in FunCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {FunCaptchaEnm.list_values()}")

    def captcha_handler(self, **kwargs) -> dict:
        """
        Sync solving method

        Args:
            kwargs: additional params for `requests` library

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
