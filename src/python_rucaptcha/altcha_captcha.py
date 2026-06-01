from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enums import AltchaEnm


class AltchaCaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        method: Union[str, AltchaEnm] = AltchaEnm.AltchaTaskProxyless,
        challengeURL: Optional[str] = None,
        challengeJSON: Optional[str] = None,
        proxyType: Optional[str] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with ALTCHA captcha.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            method: Captcha type
            challengeURL: Full URL of the page that contains ALTCHA challenge
            challengeJSON: JSON-encoded ALTCHA challenge data
            proxyType: Proxy type (http, https, socks4, socks5)
            proxyAddress: Proxy IP address or hostname
            proxyPort: Proxy port
            proxyLogin: Proxy login
            proxyPassword: Proxy password
            kwargs: Not required params for task creation request

        Examples:
            >>> AltchaCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://example.com",
            ...             challengeURL="https://example.com/altcha/challenge.js",
            ...             method=AltchaEnm.AltchaTaskProxyless.value,
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"..."
               },
               "cost":"0.00145",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

            >>> await AltchaCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://example.com",
            ...             challengeJSON='{"挑战数据"}',
            ...             method=AltchaEnm.AltchaTask.value,
            ...             proxyType="http",
            ...             proxyAddress="1.2.3.4",
            ...             proxyPort=8080,
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"..."
               },
               "cost":"0.00145",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-docs/altcha
        """

        super().__init__(method=method, *args, **kwargs)

        # XOR validation: exactly one of challengeURL or challengeJSON must be provided
        if not (bool(challengeURL) ^ bool(challengeJSON)):
            raise ValueError(
                "Exactly one of 'challengeURL' or 'challengeJSON' must be provided, not both or neither"
            )

        # Validate method
        if method not in AltchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {AltchaEnm.list_values()}")

        # Build task payload
        task_data = {"websiteURL": websiteURL}

        if challengeURL:
            task_data["challengeURL"] = challengeURL

        if challengeJSON:
            task_data["challengeJSON"] = challengeJSON

        # Add proxy params only for non-proxyless methods
        if method == AltchaEnm.AltchaTask.value:
            if not all([proxyType, proxyAddress, proxyPort]):
                raise ValueError(
                    "Proxy parameters (proxyType, proxyAddress, proxyPort) are required for AltchaTask"
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
