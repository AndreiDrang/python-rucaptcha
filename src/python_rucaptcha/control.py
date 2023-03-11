from typing import Optional

from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import ControlEnm
from python_rucaptcha.core.result_handler import get_sync_result, get_async_result


class Control(BaseCaptcha):
    def __init__(
        self,
        action: str,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with RuCaptcha control methods.

        Args:
            action: Control action type

        Examples:
            >>> Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...         action=ControlEnm.DEL_PINGBACK.value).domain_control(addr="all")
            {
                'captchaSolve': 'OK',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

            >>> Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...            action=ControlEnm.GET.value).report(id="73043727671")
            {
                'captchaSolve': '1',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#manage_pingback
            https://rucaptcha.com/api-rucaptcha#complain
            https://rucaptcha.com/api-rucaptcha#additional
        """

        super().__init__(action=action, *args, **kwargs)

        # check user params
        if action not in ControlEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {ControlEnm.list_values()}")

    def domain_control(self, addr: Optional[str] = None) -> dict:
        """
        Callback domains control

        Args:
            addr: URL for pingback or `all` with pingback delete param

        Examples:
            >>> Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...         action=ControlEnm.DEL_PINGBACK.value).domain_control(addr="all")
            {
                'captchaSolve': 'OK',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

            >>> Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...         action=ControlEnm.DEL_PINGBACK.value).domain_control(addr="http://mysite.com/pingback/url/")
            {
                'captchaSolve': 'OK',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

            >>> Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...         action=ControlEnm.ADD_PINGBACK.value).domain_control(addr="http://mysite.com/pingback/url/")
            {
                'captchaSolve': 'OK',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

            >>> Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...         action=ControlEnm.GET_PINGBACK.value).domain_control()
            {
                'captchaSolve': 'http://mysite.com/pingback/url/',
                'taskId': None,
                'error': False,
                'errorBody': None
            }


        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#manage_pingback
        """
        self.get_payload.update({"addr": addr})
        return get_sync_result(
            get_payload=self.get_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
            result=self.result,
        )

    async def aio_domain_control(self, addr: Optional[str] = None) -> dict:
        """
        Callback domains control

        Args:
            addr: URL for pingback or `all` with pingback delete param

        Examples:
            >>> await Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...         action=ControlEnm.DEL_PINGBACK.value).aio_domain_control(addr="all")
            {
                'captchaSolve': 'OK',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

            >>> await Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...         action=ControlEnm.DEL_PINGBACK.value).aio_domain_control(addr="http://mysite.com/pingback/url/")
            {
                'captchaSolve': 'OK',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

            >>> await Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...         action=ControlEnm.ADD_PINGBACK.value).aio_domain_control(addr="http://mysite.com/pingback/url/")
            {
                'captchaSolve': 'OK',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

            >>> await Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...         action=ControlEnm.GET_PINGBACK.value).aio_domain_control()
            {
                'captchaSolve': 'http://mysite.com/pingback/url/',
                'taskId': None,
                'error': False,
                'errorBody': None
            }


        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#manage_pingback
        """
        self.get_payload.update({"addr": addr})
        return await get_async_result(
            get_payload=self.get_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
            result=self.result,
        )

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

    def additional_methods(self, **kwargs) -> dict:
        """
        Some additional methods for control API (like balance and etc.)

        Args:
            kwargs: Additional params for method, like `id`, `ids`, more info in service docs.

        Examples:
            >>> Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...         action=ControlEnm.GETBALANCE.value).additional_methods()
            {
                'captchaSolve': '1044.23118',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#additional
        """
        for key in kwargs:
            self.get_payload.update({key: kwargs[key]})
        return get_sync_result(
            get_payload=self.get_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
            result=self.result,
        )

    async def aio_additional_methods(self, **kwargs) -> dict:
        """
        Some additional methods for control API (like balance and etc.)

        Args:
            kwargs: Additional params for method, like `id`, `ids`, more info in service docs.

        Examples:
            >>> await Control(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...         action=ControlEnm.GETBALANCE.value).aio_additional_methods()
            {
                'captchaSolve': '1044.23118',
                'taskId': None,
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#additional
        """
        for key in kwargs:
            self.get_payload.update({key: kwargs[key]})
        return await get_async_result(
            get_payload=self.get_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
            result=self.result,
        )


'''
# Async WebSocket method
class sockCaptchaControl(WebSocketRuCaptcha):
    def __init__(self, rucaptcha_key: str, allSessions: bool = None, suppressSuccess: bool = None):
        """
        Method setup WebSocket connection data
        Params description check in parent class
        """
        super().__init__(allSessions, suppressSuccess)
        self.rucaptcha_key = rucaptcha_key

    async def get_balance(self) -> dict:
        """
        The asynchronous WebSocket method return account balance.
        More info - https://wsrucaptcha.docs.apiary.io/#reference/4
        :return: Server response dict
        """
        balance_payload = ControlCaptchaSocketSer(
            **{
                "method": "balance",
            }
        )
        return await self.send_request(balance_payload.json(exclude_none=True))

    async def report(self, success: bool, captchaId: int) -> dict:
        """
        The asynchronous WebSocket method send captcha solving reports (success or fail).
        More info - https://wsrucaptcha.docs.apiary.io/#reference/2
        :param success: Is captcha solved success?
        :param captchaId: Captcha task unique id. For example - 5034284222
        :return: Server response dict
        """
        report_payload = ControlCaptchaSocketSer(
            **{
                "method": "report",
                "success": success,
                "captchaId": captchaId,
            }
        )

        return await self.send_request(report_payload.json(exclude_none=True))
'''
