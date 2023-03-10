from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import CapyPuzzleEnm


class CapyPuzzle(BaseCaptcha):
    def __init__(self, pageurl: str, captchakey: str, method: str = CapyPuzzleEnm.CAPY.value, *args, **kwargs):
        """
        The class is used to work with CapyPuzzle.

        Args:
            rucaptcha_key: User API key
            pageurl: Full URL of the captcha page
            captchakey: The value of the `captchakey` parameter you found in the code of the page
            method: Captcha type

        Examples:
            >>> CapyPuzzle(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captchakey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            ...             pageurl="https://www.capy.me/account/register/",
            ...             method=CapyPuzzleEnm.CAPY.value,
            ...             api_server="https://jp.api.capy.me/",
            ...             version="puzzle",
            ...             ).captcha_handler()
            {
               "serverAnswer": {},
               "captchaSolve": {
                  "captchakey": "PUZZLE_C...w",
                  "challengekey": "Uf....It",
                  "answer": "26x...x9mx"
               },
               "taskId": "73044748849",
               "error": False,
               "errorBody": None
            }

            >>> CapyPuzzle(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captchakey="AVATAR_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            ...             pageurl="https://www.capy.me/account/register/",
            ...             method=CapyPuzzleEnm.CAPY.value,
            ...             api_server="https://jp.api.capy.me/",
            ...             version="avatar",
            ...             ).captcha_handler()
            {
               "serverAnswer": {},
               "captchaSolve": {
                  "captchakey": "AVATART_C...w",
                  "challengekey": "Uf....It",
                  "answer": "26x...x9mx"
               },
               "taskId": "73044148849",
               "error": False,
               "errorBody": None
            }

            >>> CapyPuzzle(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captchakey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            ...             pageurl="https://www.capy.me/account/register/",
            ...             method="capy",
            ...             api_server="https://jp.api.capy.me/",
            ...             version="puzzle",
            ...             ).captcha_handler()
            {
               "serverAnswer": {},
               "captchaSolve": {
                  "captchakey": "PUZZLE_C...w",
                  "challengekey": "Uf....It",
                  "answer": "26x...x9mx"
               },
               "taskId": "73044748849",
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_capy
        """
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"captchakey": captchakey, "pageurl": pageurl})

        # check user params
        if method not in CapyPuzzleEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {CapyPuzzleEnm.list_values()}")

    def captcha_handler(self, **kwargs):
        """
        The class is used to work with CapyPuzzle.

        Args:
            kwargs: additional params for `requests` library

        Examples:
            >>> CapyPuzzle(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captchakey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            ...             pageurl="https://www.capy.me/account/register/",
            ...             method=CapyPuzzleEnm.CAPY.value,
            ...             api_server="https://jp.api.capy.me/",
            ...             version="puzzle",
            ...             ).captcha_handler()
            {
               "serverAnswer": {},
               "captchaSolve": {
                  "captchakey": "PUZZLE_C...w",
                  "challengekey": "Uf....It",
                  "answer": "26x...x9mx"
               },
               "taskId": "73044748849",
               "error": False,
               "errorBody": None
            }

            >>> CapyPuzzle(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captchakey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            ...             pageurl="https://www.capy.me/account/register/",
            ...             method=CapyPuzzleEnm.CAPY.value,
            ...             api_server="https://jp.api.capy.me/",
            ...             version="avatar",
            ...             ).captcha_handler()
            {
               "serverAnswer": {},
               "captchaSolve": {
                  "captchakey": "AVATART_C...w",
                  "challengekey": "Uf....It",
                  "answer": "26x...x9mx"
               },
               "taskId": "73044148849",
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_capy
        """

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self):
        """
        The class is used to work with CapyPuzzle.

        Examples:
            >>> await CapyPuzzle(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captchakey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            ...             pageurl="https://www.capy.me/account/register/",
            ...             method=CapyPuzzleEnm.CAPY.value,
            ...             api_server="https://jp.api.capy.me/",
            ...             version="puzzle",
            ...             ).aio_captcha_handler()
            {
               "serverAnswer": {},
               "captchaSolve": {
                  "captchakey": "PUZZLE_C...w",
                  "challengekey": "Uf....It",
                  "answer": "26x...x9mx"
               },
               "taskId": "73044748849",
               "error": False,
               "errorBody": None
            }

            >>> await CapyPuzzle(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             captchakey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            ...             pageurl="https://www.capy.me/account/register/",
            ...             method=CapyPuzzleEnm.CAPY.value,
            ...             api_server="https://jp.api.capy.me/",
            ...             version="avatar",
            ...             ).aio_captcha_handler()
            {
               "serverAnswer": {},
               "captchaSolve": {
                  "captchakey": "AVATART_C...w",
                  "challengekey": "Uf....It",
                  "answer": "26x...x9mx"
               },
               "taskId": "73044148849",
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_capy
        """
        return await self._aio_processing_response()
