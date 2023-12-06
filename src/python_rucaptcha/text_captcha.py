import logging

from .core.base import BaseCaptcha
from .core.enums import TextCaptchaEnm


class TextCaptcha(BaseCaptcha):
    def __init__(
        self,
        languagePool: str = "en",
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Text Captcha.

        Args:
            rucaptcha_key: User API key
            languagePool: Used to choose the workers for solving the captcha by their language.
                            Applicable to image-based and text-based captchas.\n
                            `en` - English-speaking workers\n
                            `rn` - Russian-speaking workers.
            kwargs: Additional not required params for this captcha type

        Examples:
            >>> TextCaptcha(rucaptcha_key="aa90...51122",
            ...             languagePool='en'
            ...             ).captcha_handler(textcaptcha="If tomorrow is Saturday, what day is today?")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "text":"SUNDAY"
               },
               "cost":0.03669,
               "ip":"46.53.241.91",
               "createTime":1695617910,
               "endTime":1695617965,
               "solveCount":2,
               "taskId":5423543
            }

            >>> TextCaptcha(rucaptcha_key="aa90...51122",
            ...             ).captcha_handler(textcaptcha="If tomorrow is Saturday, what day is today?")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "text":"SUNDAY"
               },
               "cost":0.03669,
               "ip":"46.53.241.91",
               "createTime":1695617910,
               "endTime":1695617965,
               "solveCount":2,
               "taskId":5423543
            }

            >>> await TextCaptcha(rucaptcha_key="aa90...51122",
            ...             ).aio_captcha_handler(textcaptcha="If tomorrow is Saturday, what day is today?")
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "text":"SUNDAY"
               },
               "cost":0.03669,
               "ip":"46.53.241.91",
               "createTime":1695617910,
               "endTime":1695617965,
               "solveCount":2,
               "taskId":5423543
            }

        Returns:
            Dict with full server response

        Notes:
            https://2captcha.com/api-docs/text

            https://rucaptcha.com/api-docs/text
        """

        super().__init__(method=TextCaptchaEnm.TextCaptchaTask.value, *args, **kwargs)

        self.create_task_payload.update({"languagePool": languagePool})
        logging.warning(f"{self.create_task_payload = }")

    def captcha_handler(self, textcaptcha: str, **kwargs) -> dict:
        """
        Synchronous method for captcha solving

        Args:
            textcaptcha: Captcha text

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        self.create_task_payload["task"].update({"comment": textcaptcha})
        return self._processing_response(**kwargs)

    async def aio_captcha_handler(self, textcaptcha: str) -> dict:
        """
        Asynchronous method for captcha solving

        Args:
            textcaptcha: Captcha text

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        self.create_task_payload["task"].update({"comment": textcaptcha})
        return await self._aio_processing_response()
