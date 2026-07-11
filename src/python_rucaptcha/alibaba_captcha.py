from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enums import AlibabaEnm


class AlibabaCaptcha(BaseCaptcha):
    """Solve Alibaba captcha with a proxyless or customer-provided proxy task."""

    def __init__(
        self,
        websiteURL: str,
        sceneId: str,
        prefix: str,
        method: Union[str, AlibabaEnm] = AlibabaEnm.AlibabaTaskProxyless,
        userId: Optional[str] = None,
        userUserId: Optional[str] = None,
        verifyType: Optional[str] = None,
        region: Optional[str] = None,
        userCertifyId: Optional[str] = None,
        apiGetLib: Optional[str] = None,
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
            websiteURL: Full URL of the page where Alibaba captcha is loaded.
            sceneId: Captcha scenario identifier.
            prefix: Captcha initialization prefix from the loading request.
            method: ``AlibabaTaskProxyless`` or ``AlibabaTask``.
            userId: Optional website-side user or session identifier.
            userUserId: Optional secondary user identifier.
            verifyType: Optional verification mechanism type.
            region: Optional Alibaba processing region.
            userCertifyId: Optional verification identifier.
            apiGetLib: Optional URL of the captcha JavaScript library.
            userAgent: Optional browser User-Agent.
            proxyType: Proxy type for ``AlibabaTask``.
            proxyAddress: Proxy IP address or hostname.
            proxyPort: Proxy port.
            proxyLogin: Optional proxy login.
            proxyPassword: Optional proxy password.
            kwargs: Additional task parameters.
        """
        super().__init__(method=method, *args, **kwargs)

        if method not in AlibabaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {AlibabaEnm.list_values()}")

        task_data = {"websiteURL": websiteURL, "sceneId": sceneId, "prefix": prefix}
        optional_data = {
            "userId": userId,
            "userUserId": userUserId,
            "verifyType": verifyType,
            "region": region,
            "userCertifyId": userCertifyId,
            "apiGetLib": apiGetLib,
            "userAgent": userAgent,
        }
        task_data.update({key: value for key, value in optional_data.items() if value is not None})

        if method == AlibabaEnm.AlibabaTask.value:
            if not all([proxyType, proxyAddress, proxyPort]):
                raise ValueError(
                    "Proxy parameters (proxyType, proxyAddress, proxyPort) are required for AlibabaTask"
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
        """Synchronously submit and poll the Alibaba task."""
        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self) -> dict:
        """Asynchronously submit and poll the Alibaba task."""
        return await self._aio_processing_response()
