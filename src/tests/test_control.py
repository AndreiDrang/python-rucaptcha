import pytest
from core.serializer import ResponseSer

from .conftest import CoreTest
from ..python_rucaptcha.core.enums import CaptchaControlEnm
from ..python_rucaptcha.CaptchaControl import CaptchaControl, aioCaptchaControl


class TestControl(CoreTest):
    """
    Success tests
    """

    def test_get_balance(self):
        instance = CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GETBALANCE.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.GETBALANCE.value

        result = instance.additional_methods()

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert float(result["captchaSolve"]) > 1
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_get_balance(self):
        with CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GETBALANCE.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.GETBALANCE.value

            result = instance.additional_methods()

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert float(result["captchaSolve"]) > 1
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_get_balance(self):
        instance = aioCaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GETBALANCE.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.GETBALANCE.value

        result = await instance.additional_methods()

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert float(result["captchaSolve"]) > 1
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_get_balance(self):
        async with aioCaptchaControl(
            rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GETBALANCE.value
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.GETBALANCE.value

            result = await instance.additional_methods()

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert float(result["captchaSolve"]) > 1
        assert result.keys() == ResponseSer().dict().keys()

    def test_get_solution(self):
        instance = CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GET.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.GET.value

        result = instance.additional_methods(ids=f"{self.get_random_string(5)},{self.get_random_string(5)}")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID|ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_get_solution(self):
        with CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GET.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.GET.value

            result = instance.additional_methods(ids=f"{self.get_random_string(5)},{self.get_random_string(5)}")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID|ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_get_solution(self):
        instance = aioCaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GET.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.GET.value

        result = await instance.additional_methods(ids=f"{self.get_random_string(5)},{self.get_random_string(5)}")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID|ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_get_solution(self):
        async with aioCaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GET.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.GET.value

            result = await instance.additional_methods(ids=f"{self.get_random_string(5)},{self.get_random_string(5)}")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID|ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    def test_get_cost(self):
        instance = CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GET2.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.GET2.value

        result = instance.additional_methods(ids=f"{self.get_random_string(5)},{self.get_random_string(5)}")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID|ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_get_cost(self):
        with CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GET2.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.GET2.value

            result = instance.additional_methods(ids=f"{self.get_random_string(5)},{self.get_random_string(5)}")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID|ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_get_cost(self):
        instance = aioCaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GET2.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.GET2.value

        result = await instance.additional_methods(ids=f"{self.get_random_string(5)},{self.get_random_string(5)}")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID|ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_get_cost(self):
        async with aioCaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.GET2.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.GET2.value

            result = await instance.additional_methods(ids=f"{self.get_random_string(5)},{self.get_random_string(5)}")

        print(result)
        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID|ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    def test_domains_clean(self):
        instance = CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.DEL_PINGBACK.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.DEL_PINGBACK.value

        result = instance.domain_control(addr="all")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert result["captchaSolve"] == "OK"
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_domains_clean(self):
        with CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.DEL_PINGBACK.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.DEL_PINGBACK.value

            result = instance.domain_control(addr="all")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert result["captchaSolve"] == "OK"
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_domains_clean(self):
        instance = aioCaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.DEL_PINGBACK.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.DEL_PINGBACK.value

        result = await instance.domain_control(addr="all")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert result["captchaSolve"] == "OK"
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_domains_clean(self):
        async with aioCaptchaControl(
            rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.DEL_PINGBACK.value
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.DEL_PINGBACK.value

            result = await instance.domain_control(addr="all")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert result["captchaSolve"] == "OK"
        assert result.keys() == ResponseSer().dict().keys()

    """
    Failed tests
    """

    def test_wrong_action(self):
        with pytest.raises(ValueError):
            CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=self.get_random_string(5))

    def test_context_wrong_action(self):
        with pytest.raises(ValueError):
            with CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=self.get_random_string(5)):
                pass

    @pytest.mark.asyncio
    async def test_aio_context_wrong_action(self):
        with pytest.raises(ValueError):
            with aioCaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=self.get_random_string(5)):
                pass

    @pytest.mark.asyncio
    async def test_aio_wrong_action(self):
        with pytest.raises(ValueError):
            aioCaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=self.get_random_string(5))

    def test_wrong_api(self):
        with pytest.raises(ValueError):
            CaptchaControl(rucaptcha_key=self.get_random_string(31), action=CaptchaControlEnm.GETBALANCE.value)

    def test_context_wrong_api(self):
        with pytest.raises(ValueError):
            with CaptchaControl(rucaptcha_key=self.get_random_string(31), action=CaptchaControlEnm.GETBALANCE.value):
                pass

    @pytest.mark.asyncio
    async def test_aio_context_wrong_api(self):
        with pytest.raises(ValueError):
            with aioCaptchaControl(rucaptcha_key=self.get_random_string(31), action=CaptchaControlEnm.GETBALANCE.value):
                pass

    @pytest.mark.asyncio
    async def test_aio_wrong_api(self):
        with pytest.raises(ValueError):
            aioCaptchaControl(rucaptcha_key=self.get_random_string(31), action=CaptchaControlEnm.GETBALANCE.value)

    def test_report_bad(self):
        instance = CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTBAD.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.REPORTBAD.value

        result = instance.report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_report_bad(self):
        with CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTBAD.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.REPORTBAD.value

            result = instance.report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_report_bad(self):
        instance = aioCaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTBAD.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.REPORTBAD.value

        result = await instance.report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_report_bad(self):
        async with aioCaptchaControl(
            rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTBAD.value
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.REPORTBAD.value

            result = await instance.report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_report_good(self):
        instance = CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTGOOD.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.REPORTGOOD.value

        result = instance.report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_report_good(self):
        with CaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTGOOD.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.REPORTGOOD.value

            result = instance.report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_report_good(self):
        instance = aioCaptchaControl(rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTGOOD.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == CaptchaControlEnm.REPORTGOOD.value

        result = await instance.report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_report_good(self):
        async with aioCaptchaControl(
            rucaptcha_key=self.RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTGOOD.value
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == CaptchaControlEnm.REPORTGOOD.value

            result = await instance.report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()
