from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import KeyCaptchaEnm


class BaseKeyCaptcha(BaseCaptcha):
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


class KeyCaptcha(BaseKeyCaptcha):
    """
    The class is used to work with KeyCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_keycaptcha
    """

    def captcha_handler(self, **kwargs):
        """
        The method is responsible for sending data to the server to solve the captcha
        :param kwargs: Parameters for the `requests` library
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """

        return self._processing_response(**kwargs)


class aioKeyCaptcha(BaseKeyCaptcha):

    """
    The class is used to async work with KeyCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_keycaptcha
    """

    async def captcha_handler(self):
        """
        The method is responsible for sending data to the server to solve the captcha
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        return await self._aio_processing_response()
