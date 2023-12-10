from .core.base import BaseCaptcha
from .core.enums import DataDomeSliderEnm


class DataDomeCaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        captchaUrl: str,
        userAgent: str,
        proxyType: str,
        proxyAddress: str,
        proxyPort: str,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with HCaptcha.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            captchaUrl: The value of the `src` parameter for the `iframe` element containing the captcha on the page.
            userAgent: User-Agent of your browser will be used to load the captcha. Use only modern browser's User-Agents
            proxyType: Proxy type - `http`, `socks4`, `socks5`
            proxyAddress: Proxy IP address or hostname
            proxyPort: Proxy port
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> DataDomeCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             captchaUrl="https://rucaptcha.com/demo/hcaptcha",
            ...             userAgent="https://rucaptcha.com/demo/hcaptcha",
            ...             proxyType="socks5",
            ...             proxyAddress="1.2.3.4",
            ...             proxyPort="445",
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "cookie": "datadome=4ZXwCBlyHx9ktZhSnycMF...; Path=/; Secure; SameSite=Lax"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

            >>> await DataDomeCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             captchaUrl="https://rucaptcha.com/demo/hcaptcha",
            ...             userAgent="https://rucaptcha.com/demo/hcaptcha",
            ...             proxyType="socks5",
            ...             proxyAddress="1.2.3.4",
            ...             proxyPort="445",
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "cookie": "datadome=4ZXwCBlyHx9ktZhSnycMF...; Path=/; Secure; SameSite=Lax"
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
            https://rucaptcha.com/api-docs/datadome-slider-captcha
        """
        super().__init__(method=DataDomeSliderEnm.DataDomeSliderTask, *args, **kwargs)

        self.create_task_payload["task"].update(
            {
                "websiteURL": websiteURL,
                "captchaUrl": captchaUrl,
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
