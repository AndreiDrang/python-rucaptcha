from typing import Union

from .core.base import BaseCaptcha
from .core.enums import AmazonWAFCaptchaEnm


class AmazonWAF(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        iv: str,
        context: str,
        method: Union[str, AmazonWAFCaptchaEnm] = AmazonWAFCaptchaEnm.AmazonTaskProxyless,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Amazon WAF

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            websiteKey: Key value from the page
            iv: Value iv from the page
            context: Value of context from page
            method: Captcha type

        Examples:
            >>> AmazonWAF(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...           websiteURL="https://page-with-waf.com/",
            ...           websiteKey="some-site-key",
            ...           iv="some-iv-value",
            ...           context="some-context-value").captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "captcha_voucher":"eyJ0eXAiO...oQjTnJlBvAW4",
                  "existing_token":"f8ab5749-f916-...5D8yAA39JtKVbw="
               },
               "cost":"0.00145",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":0,
               "taskId": 73243152973,
            }

            >>> AmazonWAF(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...           websiteURL="https://page-with-waf.com/",
            ...           websiteKey="some-site-key",
            ...           iv="some-iv-value",
            ...           context="some-context-value").aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "captcha_voucher":"eyJ0eXAiO...oQjTnJlBvAW4",
                  "existing_token":"f8ab5749-f916-...5D8yAA39JtKVbw="
               },
               "cost":"0.00145",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":0,
               "taskId": 73243152973,
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-docs/amazon-aws-waf-captcha
        """
        super().__init__(method=method, *args, **kwargs)

        # check user params
        if method not in AmazonWAFCaptchaEnm.list_values():
            raise ValueError(
                f"Invalid method parameter set, available - {AmazonWAFCaptchaEnm.list_values()}")
        # insert `gt` param to payload
        self.create_task_payload["task"].update(
            {
                "websiteURL": websiteURL,
                "websiteKey": websiteKey,
                "iv": iv,
                "context": context,
            }
        )

    def captcha_handler(self, **kwargs) -> dict:
        """
        Synchronous method for captcha solving

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self) -> dict:
        """
        Asynchronous method for captcha solving

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        return await self._aio_processing_response()
