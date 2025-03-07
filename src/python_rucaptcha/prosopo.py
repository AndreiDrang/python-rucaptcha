from typing import Union

from .core.base import BaseCaptcha
from .core.enums import ProsopoEnm


class Prosopo(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        method: Union[str, ProsopoEnm] = ProsopoEnm.ProsopoTaskProxyless,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Prosopo.

        Args:
            rucaptcha_key: User API key
            websiteURL: The full URL of target web page where the captcha is loaded.
                            We do not open the page, not a problem if it is available
                            only for authenticated users
            websiteKey: The value of `siteKey` parameter found on the page.
            method: Captcha type

        Examples:
            >>> Prosopo(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://www.example.com/",
            ...             websiteKey="5EPQoMZEDc5LpN7gtxMMzYPTzA6UeWqL2stk1rso9gy4Ahqt",
            ...             method=ProsopoEnm.ProsopoTaskProxyless.value,
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "token": "0x00016c68747470733950547a4136",
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId":75190409731
            }

            >>> await Prosopo(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://www.example.com/",
            ...             websiteKey="5EPQoMZEDc5LpN7gtxMMzYPTzA6UeWqL2stk1rso9gy4Ahqt",
            ...             method=ProsopoEnm.ProsopoTaskProxyless.value,
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "token": "0x00016c68747470733950547a4136",
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
            https://rucaptcha.com/api-docs/prosopo-procaptcha

            https://rucaptcha.com/api-docs/prosopo-procaptcha
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update({"websiteURL": websiteURL, "websiteKey": websiteKey})

        # check user params
        if method not in ProsopoEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {ProsopoEnm.list_values()}")

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
