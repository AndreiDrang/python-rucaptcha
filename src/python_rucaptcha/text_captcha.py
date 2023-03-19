from .core.base import BaseCaptcha


class TextCaptcha(BaseCaptcha):
    def __init__(
        self,
        rucaptcha_key: str,
        language: int = 0,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Text Captcha.

        Args:
            rucaptcha_key: User API key
            language: Captcha text lang:
                        0 - not defined
                        1 - captcha contains only Cyrillic
                        2 - captcha contains only latin characters

        Examples:
            >>> TextCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             language=2).captcha_handler(textcaptcha="Our planet name?")
            {
                'captchaSolve': 'earth',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

            >>> TextCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122"
            ...             ).captcha_handler(textcaptcha="Our planet name?")
            {
                'captchaSolve': 'earth',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#solving_text_captcha
        """

        super().__init__(rucaptcha_key=rucaptcha_key, *args, **kwargs)

        self.post_payload.update({"language": language})

    def captcha_handler(self, textcaptcha: str, **kwargs) -> dict:
        """
        Synchronous method for captcha solving

        Args:
            textcaptcha: Captcha text

        Examples:
            >>> TextCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             language=2).captcha_handler(textcaptcha="Our planet name?")
            {
                'captchaSolve': 'earth',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        self.post_payload.update({"textcaptcha": textcaptcha})

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self, textcaptcha: str) -> dict:
        """
        Asynchronous method for captcha solving

        Args:
            textcaptcha: Captcha text

        Examples:
            >>> await TextCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             language=2).aio_captcha_handler(textcaptcha="Our planet name?")
            {
                'captchaSolve': 'earth',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        self.post_payload.update({"textcaptcha": textcaptcha})
        return await self._aio_processing_response()
