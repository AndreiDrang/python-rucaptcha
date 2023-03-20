from .core.base import BaseCaptcha
from .core.enums import KeyCaptchaEnm


class KeyCaptcha(BaseCaptcha):
    def __init__(
        self,
        pageurl: str,
        s_s_c_user_id: str,
        s_s_c_session_id: str,
        s_s_c_web_server_sign: str,
        s_s_c_web_server_sign2: str,
        method: str = KeyCaptchaEnm.KEYCAPTCHA.value,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with KeyCaptcha.

        Args:
            rucaptcha_key: User API key
            pageurl: Full URL of the captcha page
            s_s_c_user_id: Value of `s_s_c_user_id` parameter found on the page
            s_s_c_session_id: Value of `s_s_c_session_id` parameter found on the page
            s_s_c_web_server_sign: Value of `s_s_c_web_server_sign` parameter found on the page
            s_s_c_web_server_sign2: Value of `s_s_c_web_server_sign2` parameter found on the page
            method: Captcha type
            kwargs: Not required params for task creation request

        Examples:
            >>> KeyCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://rucaptcha.com/demo/keycaptcha",
            ...             s_s_c_user_id="184015",
            ...             s_s_c_session_id="0917788cad24ad3a69813c4fcd556061",
            ...             s_s_c_web_server_sign="02f7f9669f1269595c4c69bcd4a3c52e",
            ...             s_s_c_web_server_sign2="d888700f6f324ec0f32b44c32c50bde1",
            ...             method=KeyCaptchaEnm.KEYCAPTCHA.value
            ...             ).captcha_handler()
            {
               "captchaSolve": "d58....61|1",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

            >>> await KeyCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             pageurl="https://rucaptcha.com/demo/keycaptcha",
            ...             s_s_c_user_id="184015",
            ...             s_s_c_session_id="0917788cad24ad3a69813c4fcd556061",
            ...             s_s_c_web_server_sign="02f7f9669f1269595c4c69bcd4a3c52e",
            ...             s_s_c_web_server_sign2="d888700f6f324ec0f32b44c32c50bde1",
            ...             method=KeyCaptchaEnm.KEYCAPTCHA.value
            ...             ).aio_captcha_handler()
            {
               "captchaSolve": "P1_eyJ.....cp_J",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_keycaptcha
        """
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update(
            {
                "pageurl": pageurl,
                "s_s_c_user_id": s_s_c_user_id,
                "s_s_c_session_id": s_s_c_session_id,
                "s_s_c_web_server_sign": s_s_c_web_server_sign,
                "s_s_c_web_server_sign2": s_s_c_web_server_sign2,
            }
        )

        # check user params
        if method not in KeyCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {KeyCaptchaEnm.list_values()}")

    def captcha_handler(self, **kwargs):
        """
        Sync solving method

        Args:
            kwargs: Parameters for the `requests` library

        Examples:
            >>> KeyCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             sitekey="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             pageurl="https://rucaptcha.com/demo/hcaptcha",
            ...             method=KeyCaptchaEnm.KEYCAPTCHA.value
            ...             ).captcha_handler()
            {
               "captchaSolve": "P1_eyJ.....cp_J",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_hcaptcha
        """

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self):
        """
        Async solving method

        Examples:
            >>> KeyCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             sitekey="3ceb8624-1970-4e6b-91d5-70317b70b651",
            ...             pageurl="https://rucaptcha.com/demo/hcaptcha",
            ...             method=KeyCaptchaEnm.KEYCAPTCHA.value
            ...             ).captcha_handler()
            {
               "captchaSolve": "P1_eyJ.....cp_J",
               "taskId": 73052314114,
               "error": False,
               "errorBody": None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_hcaptcha
        """
        return await self._aio_processing_response()
