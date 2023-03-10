from python_rucaptcha.core.base import BaseCaptcha


class TextCaptcha(BaseCaptcha):
    """
    The class is used to work with TextCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_text_captcha

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
            'serverAnswer': {},
            'captchaSolve': 'earth',
            'taskId': '73043008354',
            'error': False,
            'errorBody': None
        }

        >>> TextCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122")\
        ...             .captcha_handler(textcaptcha="Our planet name?")
        {
            'serverAnswer': {},
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

    def __init__(
        self,
        rucaptcha_key: str,
        language: int = 0,
        *args,
        **kwargs,
    ):
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
                'serverAnswer': {},
                'captchaSolve': 'earth',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

        Returns:
            Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name

        Notes:
            Check class docstirng for more info
        """
        self.post_payload.update({"textcaptcha": textcaptcha})

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self, textcaptcha: str) -> dict:
        """
        Asynchronous method for captcha solving

        Args:
            :param textcaptcha: Captcha text

        Examples:
            >>> await TextCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             language=2).aio_captcha_handler(textcaptcha="Our planet name?")
            {
                'serverAnswer': {},
                'captchaSolve': 'earth',
                'taskId': '73043008354',
                'error': False,
                'errorBody': None
            }

        Returns:
            Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name

        Notes:
            Check class docstirng for more info
        """
        self.post_payload.update({"textcaptcha": textcaptcha})
        return await self._aio_processing_response()
