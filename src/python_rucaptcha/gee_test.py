from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enums import GeetestEnm


class GeeTest(BaseCaptcha):
    def __init__(
        self,
        websiteURL: str,
        method: Union[GeetestEnm, str],
        gt: str,
        version: int = 3,
        initParameters: dict = None,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with GeeTest.

        Args:
            rucaptcha_key: User API key
            websiteURL: Full URL of the captcha page
            gt: The value of the `gt` parameter found on the site
            version: GeeTest V4 captcha should be set to 4.
            initParameters: Required for GeeTest V4. The parameter that is passed in the initGeetest4 function call must contain the captcha_id value.
                    Example of usage: { "captcha_id" : "e392e1d7fd421dc63325744d5a2b9c73"}
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> import requests
            >>> resp_data = requests.get("https://www.geetest.com/demo/gt/register-enFullpage-official").json()
            >>> print(resp_data)
            {
                'success': 1,
                'challenge': '1ad03db8aff920037fb8117827eab171',
                'gt': '022397c99c9f646f6477822485f30404',
                'new_captcha': True
            }
            >>> GeeTest(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             gt=resp_data["gt"],
            ...             pageurl="https://www.geetest.com/en/demo",
            ...             method=GeetestEnm.GeeTestTaskProxyless.value,
            ...             api_server="api.geetest.com",
            ...             new_captcha=1,
            ...             ).captcha_handler(challenge=resp_data["challenge"])
            {
               "captchaSolve": {
                  "geetest_challenge": "1ad03db8aff920037fb8117827eab171gu",
                  "geetest_validate": "011309d29dab6e98e8fc3784a95469cc",
                  "geetest_seccode": "011309d29dab6e98e8fc3784a95469cc|jordan"
               },
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

            >>> import requests
            >>> resp_data = requests.get("https://www.geetest.com/demo/gt/register-enFullpage-official").json()
            >>> print(resp_data)
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "captcha_id":"e392e1d7fd421dc63325744d5a2b9c73",
                  "lot_number":"e6c3bed2854f41f880662c48afff5dcb",
                  "pass_token":"fad5eb52fc83bf7617402fcccfb211a21e0aa1d1044",
                  "gen_time":"1693924478",
                  "captcha_output":"fN36ufW6cQN4SQ-JRDQC70nSq9UcQBg=="
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId":75190409731
            }
            >>> await GeeTest(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             gt=resp_data["gt"],
            ...             pageurl="https://www.geetest.com/en/demo",
            ...             method=GeetestEnm.GeeTestTaskProxyless.value,
            ...             api_server="api.geetest.com",
            ...             new_captcha=1,
            ...             ).aio_captcha_handler(challenge=resp_data["challenge"])
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "captcha_id":"e392e1d7fd421dc63325744d5a2b9c73",
                  "lot_number":"e6c3bed2854f41f880662c48afff5dcb",
                  "pass_token":"fad5eb52fc83bf7617402fcccfb211a21e0aa1d1044",
                  "gen_time":"1693924478",
                  "captcha_output":"fN36ufW6cQN4SQ-JRDQC70nSq9UcQBg=="
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId":75190409731
            }

            >>> GeeTest(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captcha_id="e392e1d7fd421dc63325744d5a2b9c73",
            ...             pageurl="https://rucaptcha.com/demo/geetest-v4",
            ...             method=GeetestEnm.GeeTestTaskProxyless.value,
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "captcha_id":"e392e1d7fd421dc63325744d5a2b9c73",
                  "lot_number":"e6c3bed2854f41f880662c48afff5dcb",
                  "pass_token":"fad5eb52fc83bf7617402fcccfb211a21e0aa1d1044",
                  "gen_time":"1693924478",
                  "captcha_output":"fN36ufW6cQN4SQ-JRDQC70nSq9UcQBg=="
               },
               "cost":"0.00299",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":1,
               "taskId":75190409731
            }

            >>> await GeeTest(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captcha_id="e392e1d7fd421dc63325744d5a2b9c73",
            ...             pageurl="https://rucaptcha.com/demo/geetest-v4",
            ...             method=GeetestEnm.GeeTestTaskProxyless.value,
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "captcha_id":"e392e1d7fd421dc63325744d5a2b9c73",
                  "lot_number":"e6c3bed2854f41f880662c48afff5dcb",
                  "pass_token":"fad5eb52fc83bf7617402fcccfb211a21e0aa1d1044",
                  "gen_time":"1693924478",
                  "captcha_output":"fN36ufW6cQN4SQ-JRDQC70nSq9UcQBg=="
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
            https://rucaptcha.com/api-docs/geetest
        """
        self.method = method
        super().__init__(method=self.method, *args, **kwargs)
        # check user params
        if self.method not in GeetestEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {GeetestEnm.list_values()}")

        # insert `gt` param to payload
        self.create_task_payload["task"].update(
            {
                "websiteURL": websiteURL,
                "gt": gt,
                "version": version,
                "initParameters": initParameters,
            }
        )

    def captcha_handler(self, challenge: Optional[str] = None, **kwargs) -> dict:
        """
        Sync solving method

        Args:
            challenge: The value of the challenge parameter found on the site
            kwargs: Parameters for the `requests` library

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        if self.method == GeetestEnm.GeeTestTaskProxyless.value:
            if challenge is not None:
                self.create_task_payload["task"].update({"challenge": challenge})
            else:
                raise ValueError(f"For {self.method} challenge is required")

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self, challenge: Optional[str] = None) -> dict:
        """
        Async solving method

        Args:
            challenge: The value of the challenge parameter found on the site

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        if self.method == GeetestEnm.GeeTestTaskProxyless.value:
            if challenge is not None:
                self.create_task_payload["task"].update({"challenge": challenge})
            else:
                raise ValueError(f"For {self.method} challenge is required")

        return await self._aio_processing_response()
