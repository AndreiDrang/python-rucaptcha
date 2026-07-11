from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enums import BasiliskEnm


class BasiliskCaptcha(BaseCaptcha):
    """Solve Basilisk captcha with a proxyless or customer-provided proxy task."""

    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        method: Union[str, BasiliskEnm] = BasiliskEnm.BasiliskTaskProxyless,
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
        Args:
            rucaptcha_key: User API key.
            websiteURL: Full URL of the page where Basilisk is loaded.
            websiteKey: The page's Basilisk data-sitekey value.
            method: ``BasiliskTaskProxyless`` or ``BasiliskTask``.
            userAgent: Optional browser User-Agent.
            proxyType: Proxy type for ``BasiliskTask``.
            proxyAddress: Proxy IP address or hostname.
            proxyPort: Proxy port.
            proxyLogin: Optional proxy login.
            proxyPassword: Optional proxy password.
            kwargs: Additional task parameters.
        """
        super().__init__(method=method, *args, **kwargs)

        if method not in BasiliskEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {BasiliskEnm.list_values()}")

        task_data = {"websiteURL": websiteURL, "websiteKey": websiteKey}
        if userAgent is not None:
            task_data["userAgent"] = userAgent

        if method == BasiliskEnm.BasiliskTask.value:
            if not all([proxyType, proxyAddress, proxyPort]):
                raise ValueError(
                    "Proxy parameters (proxyType, proxyAddress, proxyPort) are required for BasiliskTask"
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
        """Synchronously submit and poll the Basilisk task."""
        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self) -> dict:
        """Asynchronously submit and poll the Basilisk task."""
        return await self._aio_processing_response()
