from typing import Union

from .core.base import BaseCaptcha
from .core.enums import atbCaptchaEnm


class atbCaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        appId: str,
        apiServer: str,
        method: Union[str, atbCaptchaEnm] = atbCaptchaEnm.AtbCaptchaTaskProxyless,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with CapyPuzzle.

        Args:
            rucaptcha_key: User API key
            websiteURL: The full URL of target web page where the captcha is loaded.
                            We do not open the page, not a problem if it is available only for authenticated users
            appId: The value of `appId` parameter in the website source code.
            apiServer: The value of `apiServer` parameter in the website source code.
            method: Captcha type

        Examples:
            >>> atbCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://www.tencentcloud.com/account/register",
            ...             appId="2009899766",
            ...             apiServer="https://cap.aisecurius.com",
            ...             method=atbCaptchaEnm.AtbCaptchaTaskProxyless.value,
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "token": "sl191suxzluwxxh6f:"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId":75190409731
            }

            >>> await atbCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://www.tencentcloud.com/account/register",
            ...             appId="2009899766",
            ...             apiServer="https://cap.aisecurius.com",
            ...             method=atbCaptchaEnm.AtbCaptchaTaskProxyless.value,
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                    "token": "sl191suxzluwxxh6f:"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId":75190409731
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-docs/atb-captcha
            https://2captcha.com/api-docs/atb-captcha
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update(
            {"websiteURL": websiteURL, "appId": appId, "apiServer": apiServer}
        )

        # check user params
        if method not in atbCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {atbCaptchaEnm.list_values()}")

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
