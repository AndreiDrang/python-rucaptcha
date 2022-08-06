import pytest

from .conftest import CoreTest
from ..python_rucaptcha.enums import CaptchaControlEnm
from ..python_rucaptcha.serializer import ResponseSer
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
