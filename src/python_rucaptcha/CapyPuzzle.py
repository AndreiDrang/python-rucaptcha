from .base import BaseCaptcha
from .enums import CapyPuzzleEnm


class BaseCapyPuzzle(BaseCaptcha):
    def __init__(self, pageurl: str, captchakey: str, method: str = CapyPuzzleEnm.CAPY.value, *args, **kwargs):
        super().__init__(method=method, *args, **kwargs)

        self.post_payload.update({"captchakey": captchakey, "pageurl": pageurl})

        # check user params
        if method not in CapyPuzzleEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {CapyPuzzleEnm.list_values()}")


class CapyPuzzle(BaseCapyPuzzle):
    """
    The class is used to work with CapyPuzzle.
    Capy is a captcha in the form of a puzzle
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_capy
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


class aioCapyPuzzle(BaseCapyPuzzle):
    """
    Class for async solve CapyPuzzle captcha
    Capy is a captcha in the form of a puzzle
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_capy
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
