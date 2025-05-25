from .core.base import BaseCaptcha
from .core.enums import CaptchaFoxEnm


class CaptchaFox(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        userAgent: str,
        proxyType: str,
        proxyAddress: str,
        proxyPort: str,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with CaptchaFox.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            websiteKey: The value of the `key` parameter.
                            It can be found in the page source code or captured in network requests during page loading.
            userAgent: User-Agent of your browser will be used to load the captcha.
                            Use only modern browser's User-Agents
            proxyType: Proxy type - `http`, `socks4`, `socks5`
            proxyAddress: Proxy IP address or hostname
            proxyPort: Proxy port
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> CaptchaFox(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             websiteKey="sk_xtNxpk6fCdFbxh1_xJeGflSdCE9tn99G",
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

            >>> await CaptchaFox(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             websiteKey="sk_xtNxpk6fCdFbxh1_xJeGflSdCE9tn99G",
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
            https://2captcha.com/api-docs/captchafox

            https://rucaptcha.com/api-docs/captchafox
        """
        super().__init__(method=CaptchaFoxEnm.CaptchaFoxTask, *args, **kwargs)

        self.create_task_payload["task"].update(
            {
                "websiteURL": websiteURL,
                "websiteKey": websiteKey,
                "userAgent": userAgent,
                "proxyType": proxyType,
                "proxyAddress": proxyAddress,
                "proxyPort": proxyPort,
            }
        )

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
