from .base import BaseCaptcha


class BaseTextCaptcha(BaseCaptcha):
    def __init__(
        self,
        language: int = 0,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.post_payload.update({"language": language})


class TextCaptcha(BaseTextCaptcha):
    """
    The class is used to work with TextCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_text_captcha
    """

    def captcha_handler(self, textcaptcha: str, **kwargs):
        """
        The method is responsible for sending data to the server to solve the captcha
        :param kwargs: Parameters for the `requests` library
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        self.post_payload.update({"textcaptcha": textcaptcha})

        return self._processing_response(**kwargs)


class aioTextCaptcha(BaseTextCaptcha):
    """
    The class is used to async work with TextCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_text_captcha
    """

    async def captcha_handler(self, textcaptcha: str):
        """
        The method is responsible for sending data to the server to solve the captcha
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        self.post_payload.update({"textcaptcha": textcaptcha})
        return await self._aio_processing_response()


'''class sockTextCaptcha(WebSocketRuCaptcha):
    def __init__(self, rucaptcha_key: str):
        """
        The asynchronous WebSocket module is responsible for text captcha solving.
        :param rucaptcha_key: Key from RuCaptcha
        """
        super().__init__()
        self.rucaptcha_key = rucaptcha_key

    async def captcha_handler(self, captcha_text: str, **kwargs) -> dict:
        """
        The asynchronous WebSocket method return account balance.
        More info - https://wsrucaptcha.docs.apiary.io/#reference/text-captcha
        :param captcha_text: Text captcha task string
        :param kwargs: Options variables
        :return: Server response dict
        """
        text_captcha_payload = TextCaptchaSer(
            **{
                "method": "text",
                "requestId": str(uuid4()),
                "text": captcha_text,
                "options": CaptchaOptionsSer(**kwargs),
            }
        )
        return await self.send_request(text_captcha_payload.dict())
'''
