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
            >>> Control(rucaptcha_key="aa9.....",
            ...            action=ControlEnm.getBalance.value).report()
            {
                'captchaSolve': '1',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-docs/get-balance
            https://rucaptcha.com/api-docs/report-correct
            https://rucaptcha.com/api-docs/report-incorrect
        """

        super().__init__(method=ControlEnm.control, *args, **kwargs)

    def report(self, id: str) -> dict:
        """
        Captcha results report

        Args:
            id: Captcha task ID

        Examples:
            >>> Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...            action=ControlEnm.GET.value).report(id="73043727671")
            {
                'captchaSolve': '1',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

            >>> Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             action=ControlEnm.REPORTGOOD.value).report(id="73043727671")
            {
                'captchaSolve': 'OK_REPORT_RECORDED',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

            >>> Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             action=ControlEnm.REPORTBAD.value).report(id="73043727671")
            {
                'captchaSolve': 'OK_REPORT_RECORDED',
                'taskId': None,
                'error': False,
                'errorBody': None
            }


        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#complain
        """
        self.get_payload.update({"id": id})
        return get_sync_result(
            get_payload=self.get_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
            result=self.result,
        )

    async def aio_report(self, id: str) -> dict:
        """
        Captcha results report

        Args:
            id: Captcha task ID

        Examples:
            >>> await Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                 action=ControlEnm.GET.value).aio_report(id="73043727671")
            {
                'captchaSolve': '1',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

            >>> await Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                 action=ControlEnm.REPORTGOOD.value).aio_report(id="73043727671")
            {
                'captchaSolve': 'OK_REPORT_RECORDED',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

            >>> await Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...                 action=ControlEnm.REPORTBAD.value).aio_report(id="73043727671")
            {
                'captchaSolve': 'OK_REPORT_RECORDED',
                'taskId': None,
                'error': False,
                'errorBody': None
            }


        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#complain
        """
        self.get_payload.update({"id": id})
        return await get_async_result(
            get_payload=self.get_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
            result=self.result,
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
