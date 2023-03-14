import pytest

from tests.conftest import BaseTest
from python_rucaptcha.control import Control
from python_rucaptcha.core.enums import ControlEnm
from python_rucaptcha.core.serializer import ResponseSer


class TestControl(BaseTest):
    """
    Success tests
    """

    def test_methods_exists(self):
        assert "domain_control" in Control.__dict__.keys()
        assert "aio_domain_control" in Control.__dict__.keys()
        assert "report" in Control.__dict__.keys()
        assert "aio_report" in Control.__dict__.keys()
        assert "additional_methods" in Control.__dict__.keys()
        assert "aio_additional_methods" in Control.__dict__.keys()

    def test_get_balance(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GETBALANCE.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.GETBALANCE.value

        result = instance.additional_methods()

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert float(result["captchaSolve"]) > 1
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_get_balance(self):
        with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GETBALANCE.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.GETBALANCE.value

    @pytest.mark.asyncio
    async def test_aio_get_balance(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GETBALANCE.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.GETBALANCE.value

        result = await instance.aio_additional_methods()

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert float(result["captchaSolve"]) > 1
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_get_balance(self):
        async with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GETBALANCE.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.GETBALANCE.value

    def test_get_solution(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GET.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.GET.value

        result = instance.additional_methods(ids={self.get_random_string(5)})

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_get_solution(self):
        with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GET.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.GET.value

    @pytest.mark.asyncio
    async def test_aio_get_solution(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GET.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.GET.value

        result = await instance.aio_additional_methods(ids=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_get_solution(self):
        async with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GET.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.GET.value

    def test_get_cost(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GET2.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.GET2.value

        result = instance.additional_methods(ids=f"{self.get_random_string(5)},{self.get_random_string(5)}")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID|ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_get_cost(self):
        with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GET2.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.GET2.value

    @pytest.mark.asyncio
    async def test_aio_get_cost(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GET2.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.GET2.value

        result = await instance.aio_additional_methods(ids=f"{self.get_random_string(5)},{self.get_random_string(5)}")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], str) is True
        assert result["captchaSolve"] == "ERROR_NO_SUCH_CAPCHA_ID|ERROR_NO_SUCH_CAPCHA_ID"
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_get_cost(self):
        async with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.GET2.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.GET2.value

    def test_domains_clean(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.DEL_PINGBACK.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.DEL_PINGBACK.value

        result = instance.domain_control(addr="all")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert result["captchaSolve"] == "OK"
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_domains_clean(self):
        with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.DEL_PINGBACK.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.DEL_PINGBACK.value

    @pytest.mark.asyncio
    async def test_aio_domains_clean(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.DEL_PINGBACK.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.DEL_PINGBACK.value

        result = await instance.aio_domain_control(addr="all")

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"] is None
        assert result["errorBody"] is None
        assert result["captchaSolve"] == "OK"
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_domains_clean(self):
        async with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.DEL_PINGBACK.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.DEL_PINGBACK.value

    """
    Failed tests
    """

    def test_wrong_action(self):
        with pytest.raises(ValueError):
            Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=self.get_random_string(5))

    def test_context_wrong_action(self):
        with pytest.raises(ValueError):
            with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=self.get_random_string(5)):
                pass

    @pytest.mark.asyncio
    async def test_aio_context_wrong_action(self):
        with pytest.raises(ValueError):
            with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=self.get_random_string(5)):
                pass

    @pytest.mark.asyncio
    async def test_aio_wrong_action(self):
        with pytest.raises(ValueError):
            Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=self.get_random_string(5))

    def test_report_bad(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.REPORTBAD.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.REPORTBAD.value

        result = instance.report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_report_bad(self):
        with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.REPORTBAD.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.REPORTBAD.value

    @pytest.mark.asyncio
    async def test_aio_report_bad(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.REPORTBAD.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.REPORTBAD.value

        result = await instance.aio_report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_report_bad(self):
        async with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.REPORTBAD.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.REPORTBAD.value

    def test_report_good(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.REPORTGOOD.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.REPORTGOOD.value

        result = instance.report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_report_good(self):
        with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.REPORTGOOD.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.REPORTGOOD.value

    @pytest.mark.asyncio
    async def test_aio_report_good(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.REPORTGOOD.value)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.params.action == ControlEnm.REPORTGOOD.value

        result = await instance.aio_report(id=self.get_random_string(5))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == "ERROR_WRONG_CAPTCHA_ID"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_report_good(self):
        async with Control(rucaptcha_key=self.RUCAPTCHA_KEY, action=ControlEnm.REPORTGOOD.value) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.params.action == ControlEnm.REPORTGOOD.value
