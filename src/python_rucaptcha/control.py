from .core.base import BaseCaptcha
from .core.enums import ControlEnm
from .core.result_handler import get_sync_result, get_async_result


class Control(BaseCaptcha):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with RuCaptcha control methods.

        Args:
            action: Control action type

        Examples:
            >>> Control(rucaptcha_key="aa9.....").getBalance()
            {
                'balance': 1593.4479
            }

            >>> await Control(rucaptcha_key="aa9.....").aio_getBalance()
            {
                'balance': 1593.4479
            }

            >>> Control(rucaptcha_key="aa9.....").reportCorrect(id=75188571838)
            {
                'errorId': 0,
                'status': 'success'
            }

            >>> await Control(rucaptcha_key="aa9.....").aio_reportCorrect(id=75188571838)
            {
                'errorId': 0,
                'status': 'success'
            }

            >>> Control(rucaptcha_key="aa9.....").reportIncorrect(id=75188571838)
            {
                'errorId': 0,
                'status': 'success'
            }

            >>> await Control(rucaptcha_key="aa9.....").aio_reportIncorrect(id=75188571838)
            {
                'errorId': 0,
                'status': 'success'
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-docs/get-balance
            https://rucaptcha.com/api-docs/report-correct
            https://rucaptcha.com/api-docs/report-incorrect
        """

        super().__init__(method=ControlEnm.control, *args, **kwargs)

    def reportCorrect(self, id: int) -> dict:
        """
        reportCorrect method

        Args:
            id: Captcha task ID

        Returns:
            Dict with full server response

        Notes:
            https://2captcha.com/api-docs/report-correct
        """
        self.get_task_payload.taskId = id
        return get_sync_result(
            get_payload=self.get_task_payload,
            sleep_time=self.params.sleep_time,
            url_response=f"https://api.{self.params.service_type}.com/reportCorrect",
        )

    async def aio_reportCorrect(self, id: int) -> dict:
        """
        Captcha results report

        Args:
            id: Captcha task ID

        Returns:
            Dict with full server response

        Notes:
            https://2captcha.com/api-docs/report-correct
        """
        self.get_task_payload.taskId = id
        return await get_async_result(
            get_payload=self.get_task_payload,
            sleep_time=self.params.sleep_time,
            url_response=f"https://api.{self.params.service_type}.com/reportCorrect",
        )

    def reportIncorrect(self, id: int) -> dict:
        """
        reportCorrect method

        Args:
            id: Captcha task ID

        Returns:
            Dict with full server response

        Notes:
            https://2captcha.com/api-docs/report-incorrect
        """
        self.get_task_payload.taskId = id
        return get_sync_result(
            get_payload=self.get_task_payload,
            sleep_time=self.params.sleep_time,
            url_response=f"https://api.{self.params.service_type}.com/reportIncorrect",
        )

    async def aio_reportIncorrect(self, id: int) -> dict:
        """
        Captcha results report

        Args:
            id: Captcha task ID

        Returns:
            Dict with full server response

        Notes:
            https://2captcha.com/api-docs/report-incorrect
        """
        self.get_task_payload.taskId = id
        return await get_async_result(
            get_payload=self.get_task_payload,
            sleep_time=self.params.sleep_time,
            url_response=f"https://api.{self.params.service_type}.com/reportIncorrect",
        )

    def getBalance(self) -> dict:
        """
        GetBalance method

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        return get_sync_result(
            get_payload=self.get_task_payload,
            sleep_time=self.params.sleep_time,
            url_response=f"https://api.{self.params.service_type}.com/getBalance",
        )

    async def aio_getBalance(self) -> dict:
        """
        Async GetBalance method

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        return get_sync_result(
            get_payload=self.get_task_payload,
            sleep_time=self.params.sleep_time,
            url_response=f"https://api.{self.params.service_type}.com/getBalance",
        )
