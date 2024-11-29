from typing import Union

from .core.base import BaseCaptcha
from .core.enums import ReCaptchaEnm


class ReCaptcha(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        minScore: float = 0.3,
        method: Union[str, ReCaptchaEnm] = ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with ReCaptcha

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            websiteKey: The value of the `data-sitekey` parameter you found in the page code
            version: `v3` - indicates that this is reCAPTCHA V3
            method: Captcha type

        Examples:
            >>> ReCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://rucaptcha.com/demo/recaptcha-v2",
            ...             websiteKey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH",
            ...             method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "gRecaptchaResponse":"03ADUVZw...UWxTAe6ncIa",
                  "token":"03ADUVZw...UWxTAe6ncIa"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73043008354
            }

            >>> ReCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://rucaptcha.com/demo/recaptcha-v2",
            ...             websiteKey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH"
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "gRecaptchaResponse":"03ADUVZw...UWxTAe6ncIa",
                  "token":"03ADUVZw...UWxTAe6ncIa"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73043008354
            }

            >>> ReCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://rucaptcha.com/demo/recaptcha-v2",
            ...             websiteKey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH",
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "gRecaptchaResponse":"03ADUVZw...UWxTAe6ncIa",
                  "token":"03ADUVZw...UWxTAe6ncIa"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73043008354
            }

            >>> ReCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://rucaptcha.com/demo/recaptcha-v2",
            ...             websiteKey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH",
            ...             method=ReCaptchaEnm.RecaptchaV3TaskProxyless.value,
            ...             min_score=0.3,
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "gRecaptchaResponse":"03ADUVZw...UWxTAe6ncIa",
                  "token":"03ADUVZw...UWxTAe6ncIa"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73043008354
            }

            >>> await ReCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteURL="https://rucaptcha.com/demo/recaptcha-v2",
            ...             websiteKey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH",
            ...             method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "gRecaptchaResponse":"03ADUVZw...UWxTAe6ncIa",
                  "token":"03ADUVZw...UWxTAe6ncIa"
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId": 73043008354
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-docs/recaptcha-v2

            https://rucaptcha.com/api-docs/recaptcha-v3

            https://rucaptcha.com/api-docs/recaptcha-v2-enterprise
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update(
            {"websiteURL": websiteURL, "websiteKey": websiteKey, "minScore": minScore}
        )

        # check user params
        if method not in ReCaptchaEnm.list_values():
            raise ValueError(
                f"Invalid method parameter set, available - {ReCaptchaEnm.list_values()}")

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
