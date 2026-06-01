from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enums import YidunEnm


class YidunCaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        method: Union[str, YidunEnm] = YidunEnm.YidunTaskProxyless,
        userAgent: Optional[str] = None,
        yidunGetLib: Optional[str] = None,
        yidunApiServerSubdomain: Optional[str] = None,
        challenge: Optional[str] = None,
        hcg: Optional[str] = None,
        hct: Optional[int] = None,
        proxyType: Optional[str] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Yidun NECaptcha.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the page where the captcha is loaded
            websiteKey: Value of the `id` (or `sitekey`) parameter from the page source
                        or from the `get?referer=` / `check?referer=` network request
            method: Captcha type (YidunTaskProxyless or YidunTask)
            userAgent: Browser User-Agent used to open the page
            yidunGetLib: Full URL of the JS file that loads the captcha.
                         Recommended for Enterprise version.
            yidunApiServerSubdomain: Yidun API server subdomain without `https://`.
                         Specify if using a custom server.
            challenge: Dynamic challenge parameter from network requests (Enterprise)
            hcg: Captcha hash used when forming the request (Enterprise)
            hct: Numeric timestamp identifier for Enterprise version validation (Unix milliseconds)
            proxyType: Proxy type (http, socks4, socks5) - required for YidunTask
            proxyAddress: Proxy IP or hostname - required for YidunTask
            proxyPort: Proxy port - required for YidunTask
            proxyLogin: Proxy login (optional)
            proxyPassword: Proxy password (optional)

        Examples:
            >>> YidunCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://example.com/page-with-yidun",
            ...             websiteKey="0f743r3g1g...rz3grz0ym5",
            ...             method=YidunEnm.YidunTaskProxyless.value,
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"D19scz7n4VCU7b_...fRyEY-tXQ0cmS6laRKp_tZEyei_EUzc5M1IW0oxUHnZ4fBMH2a0jMPjOReiHVWBgkrcRYaOkQRasHlFejEToe7HZJy2jaGkxiB9b"
               },
               "cost":"0.003",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

            >>> await YidunCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                     websiteURL="https://example.com/page-with-yidun",
            ...                     websiteKey="0f743r3g1g...rz3grz0ym5",
            ...                     method=YidunEnm.YidunTask.value,
            ...                     proxyType="http",
            ...                     proxyAddress="1.2.3.4",
            ...                     proxyPort=8080,
            ...                     ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"D19scz7n4VCU7b_...fRyEY-tXQ0cmS6laRKp_tZEyei_EUzc5M1IW0oxUHnZ4fBMH2a0jMPjOReiHVWBgkrcRYaOkQRasHlFejEToe7HZJy2jaGkxiB9b"
               },
               "cost":"0.003",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

        Returns:
            Dict with full server response

        Notes:
            https://2captcha.com/api-docs/yidun-necaptcha

            https://rucaptcha.com/api-docs/yidun-necaptcha
        """
        super().__init__(method=method, *args, **kwargs)

        # Validate method
        if method not in YidunEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {YidunEnm.list_values()}")

        # Build task payload
        task_data = {
            "websiteURL": websiteURL,
            "websiteKey": websiteKey,
        }

        # Optional Enterprise-version and userAgent fields (only include if non-None)
        if userAgent is not None:
            task_data["userAgent"] = userAgent
        if yidunGetLib is not None:
            task_data["yidunGetLib"] = yidunGetLib
        if yidunApiServerSubdomain is not None:
            task_data["yidunApiServerSubdomain"] = yidunApiServerSubdomain
        if challenge is not None:
            task_data["challenge"] = challenge
        if hcg is not None:
            task_data["hcg"] = hcg
        if hct is not None:
            task_data["hct"] = hct

        # Add proxy params only for non-proxyless methods
        if method == YidunEnm.YidunTask.value:
            if not all([proxyType, proxyAddress, proxyPort]):
                raise ValueError(
                    "Proxy parameters (proxyType, proxyAddress, proxyPort) are required for YidunTask"
                )
            task_data.update(
                {
                    "proxyType": proxyType,
                    "proxyAddress": proxyAddress,
                    "proxyPort": proxyPort,
                }
            )
            if proxyLogin is not None:
                task_data["proxyLogin"] = proxyLogin
            if proxyPassword is not None:
                task_data["proxyPassword"] = proxyPassword

        self.create_task_payload["task"].update(task_data)

    def captcha_handler(self, **kwargs) -> dict:
        """
        Sync solving method

        Args:
            kwargs: Parameters for the `requests` library

        Returns:
            Dict with full server response

        Notes:
            Check class docstring for more info
        """
        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self) -> dict:
        """
        Async solving method

        Returns:
            Dict with full server response

        Notes:
            Check class docstring for more info
        """
        return await self._aio_processing_response()
