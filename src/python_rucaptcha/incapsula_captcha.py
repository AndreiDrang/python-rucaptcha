from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enums import IncapsulaEnm


class IncapsulaCaptcha(BaseCaptcha):
    """Solve the cookie-based Imperva (Incapsula) captcha."""

    def __init__(
        self,
        websiteURL: str,
        incapsulaScriptUrl: str,
        incapsulaCookies: str,
        proxyType: str,
        proxyAddress: str,
        proxyPort: int,
        method: Union[str, IncapsulaEnm] = IncapsulaEnm.IncapsulaTask,
        userAgent: Optional[str] = None,
        reese84UrlEndpoint: Optional[str] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """
        Args:
            rucaptcha_key: User API key.
            websiteURL: Full URL of the page where Incapsula is loaded.
            incapsulaScriptUrl: Incapsula JavaScript resource URL or name.
            incapsulaCookies: Cookies received from the Incapsula challenge page.
            proxyType: Proxy type: ``http``, ``socks4`` or ``socks5``.
            proxyAddress: Proxy IP address or hostname.
            proxyPort: Proxy port.
            method: Captcha task type. Only ``IncapsulaTask`` is supported.
            userAgent: Optional browser User-Agent.
            reese84UrlEndpoint: Optional Reese84 fingerprint endpoint.
            proxyLogin: Optional proxy login.
            proxyPassword: Optional proxy password.
            kwargs: Additional task parameters.
        """
        super().__init__(method=method, *args, **kwargs)

        if method not in IncapsulaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {IncapsulaEnm.list_values()}")

        task_data = {
            "websiteURL": websiteURL,
            "incapsulaScriptUrl": incapsulaScriptUrl,
            "incapsulaCookies": incapsulaCookies,
            "proxyType": proxyType,
            "proxyAddress": proxyAddress,
            "proxyPort": proxyPort,
        }
        optional_data = {
            "userAgent": userAgent,
            "reese84UrlEndpoint": reese84UrlEndpoint,
            "proxyLogin": proxyLogin,
            "proxyPassword": proxyPassword,
        }
        task_data.update({key: value for key, value in optional_data.items() if value is not None})
        self.create_task_payload["task"].update(task_data)

    def captcha_handler(self, **kwargs) -> dict:
        """Synchronously submit and poll the Incapsula task."""
        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self) -> dict:
        """Asynchronously submit and poll the Incapsula task."""
        return await self._aio_processing_response()


# Imperva is the product name; keep an intuitive alias alongside the API name.
ImpervaCaptcha = IncapsulaCaptcha
ImpervaEnm = IncapsulaEnm
