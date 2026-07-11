from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enums import TSPDEnm


class TSPDCaptcha(BaseCaptcha):
    """Solve the cookie-based TSPD captcha using a static proxy session."""

    def __init__(
        self,
        websiteURL: str,
        tspdcookie: str,
        htmlPageBase64: str,
        proxyType: str,
        proxyAddress: str,
        proxyPort: int,
        method: Union[str, TSPDEnm] = TSPDEnm.TspdTask,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        userAgent: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """
        Args:
            rucaptcha_key: User API key.
            websiteURL: Full URL of the page where TSPD is loaded.
            tspdcookie: Cookies received from the TSPD challenge page.
            htmlPageBase64: Full challenge-page HTML encoded as Base64.
            proxyType: Proxy type: ``http``, ``socks4`` or ``socks5``.
            proxyAddress: Proxy IP address or hostname.
            proxyPort: Proxy port.
            method: Captcha task type. Only ``tspdtask`` is supported.
            proxyLogin: Optional proxy login.
            proxyPassword: Optional proxy password.
            userAgent: Browser User-Agent used to load the page.
            kwargs: Additional task parameters.

        Notes:
            The proxy must use a static session and the same outbound IP must be
            maintained while obtaining cookies, solving the task, and using the
            returned cookies.
        """
        super().__init__(method=method, *args, **kwargs)

        if method not in TSPDEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {TSPDEnm.list_values()}")

        task_data = {
            "websiteURL": websiteURL,
            "tspdcookie": tspdcookie,
            "htmlPageBase64": htmlPageBase64,
            "proxyType": proxyType,
            "proxyAddress": proxyAddress,
            "proxyPort": proxyPort,
        }
        if proxyLogin is not None:
            task_data["proxyLogin"] = proxyLogin
        if proxyPassword is not None:
            task_data["proxyPassword"] = proxyPassword
        if userAgent is not None:
            task_data["userAgent"] = userAgent

        self.create_task_payload["task"].update(task_data)

    def captcha_handler(self, **kwargs) -> dict:
        """Synchronously submit and poll the TSPD task."""
        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self) -> dict:
        """Asynchronously submit and poll the TSPD task."""
        return await self._aio_processing_response()
