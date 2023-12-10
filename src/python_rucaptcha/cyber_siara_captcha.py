from typing import Union

from .core.base import BaseCaptcha
from .core.enums import CyberSiARAEnm


class CyberSiARACaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        SlideMasterUrlId: str,
        userAgent: str,
        method: Union[str, CyberSiARAEnm] = CyberSiARAEnm.AntiCyberSiAraTaskProxyless.value,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with HCaptcha.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            SlideMasterUrlId: The value of the `MasterUrlId` parameter obtained from the request to the endpoint `API/CyberSiara/GetCyberSiara`.
            userAgent: User-Agent of your browser will be used to load the captcha. Use only modern browser's User-Agents
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> CyberSiARACaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             SlideMasterUrlId="https://rucaptcha.com/demo/hcaptcha",
            ...             userAgent="Mozilla/5.0 (Windows .....",
            ...             method=CyberSiARAEnm.AntiCyberSiAraTaskProxyless,
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

            >>> await CyberSiARACaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             SlideMasterUrlId="https://rucaptcha.com/demo/hcaptcha",
            ...             userAgent="Mozilla/5.0 (Windows .....",
            ...             method=CyberSiARAEnm.AntiCyberSiAraTaskProxyless,
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
            https://rucaptcha.com/api-docs/anti-cyber-siara#cybersiara
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update(
            {"websiteURL": websiteURL, "SlideMasterUrlId": SlideMasterUrlId, "userAgent": userAgent}
        )
        # check user params
        if method not in CyberSiARAEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {CyberSiARAEnm.list_values()}")

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
