from typing import Any

from .core.base import BaseCaptcha
from .core.enums import VKCaptchaEnm


class VKCaptcha(BaseCaptcha):
    def __init__(
        self,
        redirectUri: str,
        userAgent: str,
        proxyType: str,
        proxyAddress: str,
        proxyPort: str,
        *args,
        **kwargs: dict[str, Any],
    ):
        """
        The class is used to work with VKCaptchaTask.

        Args:
            rucaptcha_key: User API key
            redirectUri: The URL that is returned on requests to the captcha API.
            userAgent: User-Agent of your browser will be used to load the captcha.
                            Use only modern browser's User-Agents
            proxyType: Proxy type - `http`, `socks4`, `socks5`
            proxyAddress: Proxy IP address or hostname
            proxyPort: Proxy port
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> VKCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             redirectUri="https://id.vk.com/not_robot_captcha?domain=vk.com...",
            ...             userAgent="Mozilla/5.0 .....",
            ...             proxyType="socks5",
            ...             proxyAddress="1.2.3.4",
            ...             proxyPort="445",
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

            >>> await VKCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             redirectUri="https://id.vk.com/not_robot_captcha?domain=vk.com...",
            ...             userAgent="Mozilla/5.0 .....",
            ...             proxyType="socks5",
            ...             proxyAddress="1.2.3.4",
            ...             proxyPort="445",
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
            https://2captcha.com/api-docs/vk-captcha

            https://rucaptcha.com/api-docs/vk-captcha
        """
        super().__init__(method=VKCaptchaEnm.VKCaptchaTask, *args, **kwargs)

        self.create_task_payload["task"].update(
            {
                "websiteURL": redirectUri,
                "userAgent": userAgent,
                "proxyType": proxyType,
                "proxyAddress": proxyAddress,
                "proxyPort": proxyPort,
            }
        )

    def captcha_handler(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
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

    async def aio_captcha_handler(self) -> dict[str, Any]:
        """
        Async solving method

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        return await self._aio_processing_response()
