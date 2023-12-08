from typing import Union

from .core.base import BaseCaptcha
from .core.enums import CapyPuzzleEnm


class CapyPuzzle(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        method: Union[str, CapyPuzzleEnm] = CapyPuzzleEnm.CapyTaskProxyless,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with CapyPuzzle.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            websiteKey: The value of the `captchakey` parameter you found in the code of the page
            method: Captcha type

        Examples:
            >>> CapyPuzzle(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteKey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            ...             websiteURL="https://www.capy.me/account/register/",
            ...             method=CapyPuzzleEnm.CapyTaskProxyless.value,
            ...             api_server="https://jp.api.capy.me/",
            ...             version="puzzle",
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "captchakey":"PUZZLE_Abc1dEFghIJKLM2no34P56q7rStu8v",
                  "challengekey":"qHAPtn68KTnXFM8VQ3mtYRtmy3cSKuHJ",
                  "answer":"0xax8ex0xax84x0xkx7qx0xux7gx0xx42x0x3ox42x0x3ox4cx",
                  "respKey":""
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId":75190409731
            }

            >>> CapyPuzzle(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteKey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            ...             websiteURL="https://www.capy.me/account/register/",
            ...             method=CapyPuzzleEnm.CapyTaskProxyless.value,
            ...             api_server="https://jp.api.capy.me/",
            ...             version="avatar",
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "captchakey":"PUZZLE_Abc1dEFghIJKLM2no34P56q7rStu8v",
                  "challengekey":"qHAPtn68KTnXFM8VQ3mtYRtmy3cSKuHJ",
                  "answer":"0xax8ex0xax84x0xkx7qx0xux7gx0xx42x0x3ox42x0x3ox4cx",
                  "respKey":""
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId":75190409731
            }

            >>> CapyPuzzle(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             websiteKey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            ...             websiteURL="https://www.capy.me/account/register/",
            ...             method="CapyTaskProxyless",
            ...             api_server="https://jp.api.capy.me/",
            ...             version="puzzle",
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "captchakey":"PUZZLE_Abc1dEFghIJKLM2no34P56q7rStu8v",
                  "challengekey":"qHAPtn68KTnXFM8VQ3mtYRtmy3cSKuHJ",
                  "answer":"0xax8ex0xax84x0xkx7qx0xux7gx0xx42x0x3ox42x0x3ox4cx",
                  "respKey":""
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
            https://rucaptcha.com/api-docs/capy-puzzle-captcha
        """
        super().__init__(method=method, *args, **kwargs)

        self.create_task_payload["task"].update({"websiteURL": websiteURL, "websiteKey": websiteKey})

        # check user params
        if method not in CapyPuzzleEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {CapyPuzzleEnm.list_values()}")

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
