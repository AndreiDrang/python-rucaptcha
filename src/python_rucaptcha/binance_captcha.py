from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enums import BinanceCaptchaEnm


class BinanceCaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        validateId: str,
        method: Union[str, BinanceCaptchaEnm] = BinanceCaptchaEnm.BinanceTaskProxyless,
        userAgent: Optional[str] = None,
        proxyType: Optional[str] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Binance CAPTCHA.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the page where the captcha is loaded
            websiteKey: Value of bizId, bizType, or bizCode from page requests
            validateId: Dynamic value of validateId, securityId, or securityCheckResponseValidateId
            method: Captcha type
            userAgent: User-Agent string to be used when solving the captcha
            proxyType: Proxy type (http, https, socks4, socks5)
            proxyAddress: Proxy IP address or hostname
            proxyPort: Proxy port
            proxyLogin: Proxy login
            proxyPassword: Proxy password

        Examples:
            >>> BinanceCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://example.com/page-with-binance",
            ...             websiteKey="login",
            ...             validateId="cb0bfefa598...e54ecd57b",
            ...             userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            ...                        "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            ...             method=BinanceCaptchaEnm.BinanceTaskProxyless.value,
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"captcha#09ba4905a79f44f...kc99maS943qIsquNP9D77",
                  "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

            >>> await BinanceCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://example.com/page-with-binance",
            ...             websiteKey="login",
            ...             validateId="cb0bfefa598...e54ecd57b",
            ...             method=BinanceCaptchaEnm.BinanceTask.value,
            ...             proxyType="http",
            ...             proxyAddress="1.2.3.4",
            ...             proxyPort=8080,
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"captcha#09ba4905a79f44f...kc99maS943qIsquNP9D77",
                  "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
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
            https://2captcha.com/api-docs/binance-captcha

            https://rucaptcha.com/api-docs/binance-captcha
        """
        super().__init__(method=method, *args, **kwargs)

        # Validate method
        if method not in BinanceCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {BinanceCaptchaEnm.list_values()}")

        # Build task payload
        task_data = {
            "websiteURL": websiteURL,
            "websiteKey": websiteKey,
            "validateId": validateId,
        }

        if userAgent:
            task_data["userAgent"] = userAgent

        # Add proxy params only for non-proxyless methods
        if method == BinanceCaptchaEnm.BinanceTask.value:
            if not all([proxyType, proxyAddress, proxyPort]):
                raise ValueError(
                    "Proxy parameters (proxyType, proxyAddress, proxyPort) are required for BinanceTask"
                )
            task_data.update(
                {
                    "proxyType": proxyType,
                    "proxyAddress": proxyAddress,
                    "proxyPort": proxyPort,
                }
            )
            if proxyLogin and proxyPassword:
                task_data["proxyLogin"] = proxyLogin
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
