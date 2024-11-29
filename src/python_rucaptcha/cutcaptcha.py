from typing import Union

from .core.base import BaseCaptcha
from .core.enums import CutCaptchaEnm


class CutCaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        miseryKey: str,
        apiKey: str,
        method: Union[str, CutCaptchaEnm] = CutCaptchaEnm.CutCaptchaTaskProxyless,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with CutCaptcha.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            miseryKey: The value of CUTCAPTCHA_MISERY_KEY variable defined on page.
            apiKey: The value of data-apikey attribute of iframe's body.
                        Also the name of javascript file included on the page
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> CutCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://example.cc/foo/bar.html",
            ...             miseryKey="a1488b66da00bf332a1488993a5443c79047e752",
            ...             apiKey="SAb83IIB",
            ...             method=CutCaptchaEnm.CutCaptchaTaskProxyless
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"P1_eyJ0eXAiOiJKV...1LDq89KyJ5A",
                  "respKey":"E0_eyJ0eXAiOiJK...y2w5_YbP8PGuJBBo",
                  "userAgent":"Mozilla/5.0 (.......",
                  "gRecaptchaResponse":"P1_eyJ0eXAiOiJKV...1LDq89KyJ5A"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73243152973,
            }

            >>> await CutCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://example.cc/foo/bar.html",
            ...             miseryKey="a1488b66da00bf332a1488993a5443c79047e752",
            ...             apiKey="SAb83IIB",
            ...             method=CutCaptchaEnm.CutCaptchaTaskProxyless
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"P1_eyJ0eXAiOiJKV...1LDq89KyJ5A",
                  "respKey":"E0_eyJ0eXAiOiJK...y2w5_YbP8PGuJBBo",
                  "userAgent":"Mozilla/5.0 (........",
                  "gRecaptchaResponse":"P1_eyJ0eXAiOiJKV...1LDq89KyJ5A"
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
            https://2captcha.com/api-docs/cutcaptcha
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update({"websiteURL": websiteURL,
                                                 "miseryKey": miseryKey,
                                                 "apiKey": apiKey})

        # check user params
        if method not in CutCaptchaEnm.list_values():
            raise ValueError(
                f"Invalid method parameter set, available - {CutCaptchaEnm.list_values()}")

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
