from typing import Optional

from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import GeetestEnm


class GeeTest(BaseCaptcha):
    def __init__(
        self,
        pageurl: str,
        method: str,
        gt: Optional[str] = None,
        captcha_id: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Arkose Labs FunCaptcha.

        Args:
            rucaptcha_key: User API key
            pageurl: Full URL of the captcha page
            gt: The value of the `gt` parameter found on the site
            captcha_id: The value of the `captcha_id` parameter found on the site
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
            ...             method=GeetestEnm.GEETEST.value,
            ...             api_server="api.geetest.com",
            ...             new_captcha=1,
            ...             ).captcha_handler(challenge=resp_data["challenge"])
            {
               "captchaSolve": {
                  "geetest_challenge": "1ad03db8aff920037fb8117827eab171gu",
                  "geetest_validate": "011309d29dab6e98e8fc3784a95469cc",
                  "geetest_seccode": "011309d29dab6e98e8fc3784a95469cc|jordan"
               },
               "taskId": "73052314114",
               "error": False,
               "errorBody": None
            }

            >>> import requests
            >>> resp_data = requests.get("https://www.geetest.com/demo/gt/register-enFullpage-official").json()
            >>> print(resp_data)
            {
                'success': 1,
                'challenge': '1ad03db8aff920037fb8117827eab171',
                'gt': '022397c99c9f646f6477822485f30404',
                'new_captcha': True
            }
            >>> await GeeTest(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             gt=resp_data["gt"],
            ...             pageurl="https://www.geetest.com/en/demo",
            ...             method=GeetestEnm.GEETEST.value,
            ...             api_server="api.geetest.com",
            ...             new_captcha=1,
            ...             ).aio_captcha_handler(challenge=resp_data["challenge"])
            {
               "captchaSolve": {
                  "geetest_challenge": "1ad0....b171gu",
                  "geetest_validate": "011....69cc",
                  "geetest_seccode": "0....c|jordan"
               },
               "taskId": "73052314114",
               "error": False,
               "errorBody": None
            }

            >>> GeeTest(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captcha_id="e392e1d7fd421dc63325744d5a2b9c73",
            ...             pageurl="https://rucaptcha.com/demo/geetest-v4",
            ...             method=GeetestEnm.GEETEST_V4.value,
            ...             ).captcha_handler()
            {
                "captchaSolve": {
                    "captcha_id": "e39....73",
                    "lot_number": "1b....bd2",
                    "pass_token": "f3b....de7f",
                    "gen_time": "1678558017",
                    "captcha_output": "c3rHzKl....TE=",
                },
                "taskId": "73052937243",
                "error": False,
                "errorBody": "None",
            }

            >>> await GeeTest(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captcha_id="e392e1d7fd421dc63325744d5a2b9c73",
            ...             pageurl="https://rucaptcha.com/demo/geetest-v4",
            ...             method=GeetestEnm.GEETEST_V4.value,
            ...             ).aio_captcha_handler()
            {
                "captchaSolve": {
                    "captcha_id": "e39....73",
                    "lot_number": "1b....bd2",
                    "pass_token": "f3b....de7f",
                    "gen_time": "1678558017",
                    "captcha_output": "c3r....TE=",
                },
                "taskId": "73052937243",
                "error": False,
                "errorBody": "None",
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_geetest
            https://rucaptcha.com/api-rucaptcha#geetest-v4
        """
        self.method = method
        super().__init__(method=self.method, *args, **kwargs)
        # check user params
        if self.method not in GeetestEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {GeetestEnm.list_values()}")

        # insert `gt` param to payload
        self.post_payload.update({"gt": gt, "pageurl": pageurl, "captcha_id": captcha_id})

        if self.method == GeetestEnm.GEETEST_V4.value and captcha_id is None:
            raise ValueError(f"For {self.method} captcha_id is required")
        elif self.method == GeetestEnm.GEETEST.value and gt is None:
            raise ValueError(f"For {self.method} gt is required")

    def captcha_handler(self, challenge: Optional[str] = None, **kwargs) -> dict:
        """
        Sync solving method

        Args:
            challenge: The value of the challenge parameter found on the site
            kwargs: Parameters for the `requests` library

        Examples:
            >>> GeeTest(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             gt="022397c99c9f646f6477822485f30404",
            ...             pageurl="https://rucaptcha.com/demo/geetest",
            ...             method=GeetestEnm.GEETEST.value,
            ...             api_server="api.geetest.com",
            ...             ).captcha_handler(challenge="537b31c6ff5d2bcfa9d1b75e099edcb2")
            {
               "captchaSolve": {
                  "geetest_challenge": "1ad03db8aff920037fb8117827eab171gu",
                  "geetest_validate": "011309d29dab6e98e8fc3784a95469cc",
                  "geetest_seccode": "011309d29dab6e98e8fc3784a95469cc|jordan"
                },
               "taskId": "73045070203",
               "error": False,
               "errorBody": None
            }

            >>> GeeTest(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captcha_id="e392e1d7fd421dc63325744d5a2b9c73",
            ...             pageurl="https://rucaptcha.com/demo/geetest-v4",
            ...             method=GeetestEnm.GEETEST_V4.value,
            ...             ).captcha_handler()
            {
                "captchaSolve": {
                    "captcha_id": "e39....73",
                    "lot_number": "1b....bd2",
                    "pass_token": "f3b....de7f",
                    "gen_time": "1678558017",
                    "captcha_output": "c3rHzKl....TE=",
                },
                "taskId": "73052937243",
                "error": False,
                "errorBody": "None",
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_geetest
            https://rucaptcha.com/api-rucaptcha#geetest-v4
        """
        if self.method == GeetestEnm.GEETEST.value:
            if challenge is not None:
                self.post_payload.update({"challenge": challenge})
            else:
                raise ValueError(f"For {self.method} challenge is required")

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self, challenge: Optional[str] = None) -> dict:
        """
        Async solving method

        Args:
            challenge: The value of the challenge parameter found on the site

        Examples:
            >>> await GeeTest(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             gt="022397c99c9f646f6477822485f30404",
            ...             pageurl="https://rucaptcha.com/demo/geetest",
            ...             method=GeetestEnm.GEETEST.value,
            ...             api_server="api.geetest.com",
            ...             ).aio_captcha_handler(challenge="537b31c6ff5d2bcfa9d1b75e099edcb2")
            {
               "captchaSolve": {
                  "geetest_challenge": "1ad03db8aff920037fb8117827eab171gu",
                  "geetest_validate": "011309d29dab6e98e8fc3784a95469cc",
                  "geetest_seccode": "011309d29dab6e98e8fc3784a95469cc|jordan"
                },
               "taskId": "73045070203",
               "error": False,
               "errorBody": None
            }

            >>> await GeeTest(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captcha_id="e392e1d7fd421dc63325744d5a2b9c73",
            ...             pageurl="https://rucaptcha.com/demo/geetest-v4",
            ...             method=GeetestEnm.GEETEST_V4.value,
            ...             ).aio_captcha_handler()
            {
                "captchaSolve": {
                    "captcha_id": "e39....73",
                    "lot_number": "1b....bd2",
                    "pass_token": "f3b....de7f",
                    "gen_time": "1678558017",
                    "captcha_output": "c3rHzKl....TE=",
                },
                "taskId": "73052937243",
                "error": False,
                "errorBody": "None",
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_geetest
            https://rucaptcha.com/api-rucaptcha#geetest-v4
        """
        if self.method == GeetestEnm.GEETEST.value:
            if challenge is not None:
                self.post_payload.update({"challenge": challenge})
            else:
                raise ValueError(f"For {self.method} challenge is required")

        return await self._aio_processing_response()
