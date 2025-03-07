from typing import Union

from .core.base import BaseCaptcha
from .core.enums import TencentEnm


class Tencent(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        appId: str,
        method: Union[str, TencentEnm] = TencentEnm.TencentTaskProxyless,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with CapyPuzzle.

        Args:
            rucaptcha_key: User API key
            websiteURL: The full URL of target web page where the captcha is loaded.
                            We do not open the page, not a problem if it is available
                            only for authenticated users
            appId: The value of `appId` parameter in the website source code.
            method: Captcha type

        Examples:
            >>> Tencent(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://www.tencentcloud.com/account/register",
            ...             appId="2009899766",
            ...             method=TencentEnm.TencentTaskProxyless.value,
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "appid": "190014885",
                    "ret": 0,
                    "ticket": "tr034XXXXXXXXXXXXXXXXXX*",
                    "randstr": "@KVN"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId":75190409731
            }

            >>> await Tencent(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://www.tencentcloud.com/account/register",
            ...             appId="2009899766",
            ...             method=TencentEnm.TencentTaskProxyless.value,
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "appid": "190014885",
                    "ret": 0,
                    "ticket": "tr034XXXXXXXXXXXXXXXXXX*",
                    "randstr": "@KVN"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId":75190409731
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-docs/tencent

            https://2captcha.com/api-docs/tencent
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update({"websiteURL": websiteURL, "appId": appId})

        # check user params
        if method not in TencentEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {TencentEnm.list_values()}")

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
