import random

import pytest

from tests.conftest import BaseTest
from python_rucaptcha.control import Control
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestControl(BaseTest):
    """
    Success tests
    """

    def test_methods_exists(self):
        assert "reportCorrect" in Control.__dict__.keys()
        assert "aio_reportCorrect" in Control.__dict__.keys()
        assert "reportIncorrect" in Control.__dict__.keys()
        assert "aio_reportIncorrect" in Control.__dict__.keys()
        assert "getBalance" in Control.__dict__.keys()
        assert "getBalance" in Control.__dict__.keys()

    def test_get_balance(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = instance.getBalance()

        assert isinstance(result, dict) is True
        assert result["balance"] > 1
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_get_balance(self):
        with Control(rucaptcha_key=self.RUCAPTCHA_KEY) as instance:
            assert instance.getBalance()

    @pytest.mark.asyncio
    async def test_aio_get_balance(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = await instance.aio_getBalance()

        assert isinstance(result, dict) is True
        assert result["balance"] > 1
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_get_balance(self):
        async with Control(rucaptcha_key=self.RUCAPTCHA_KEY) as instance:
            assert await instance.aio_getBalance()

    """
    Failed tests
    """

    def test_report_bad(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = instance.reportIncorrect(id=random.randint(20, 50))
        assert isinstance(result, dict) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_report_bad(self):
        with Control(rucaptcha_key=self.RUCAPTCHA_KEY) as instance:
            assert instance.reportIncorrect(id=random.randint(20, 50))

    @pytest.mark.asyncio
    async def test_aio_report_bad(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = await instance.aio_reportIncorrect(id=random.randint(20, 50))
        assert isinstance(result, dict) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_report_bad(self):
        async with Control(rucaptcha_key=self.RUCAPTCHA_KEY) as instance:
            assert await instance.aio_reportIncorrect(id=random.randint(20, 50))

    def test_report_good(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = instance.reportCorrect(id=random.randint(20, 50))
        assert isinstance(result, dict) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_report_good(self):
        with Control(rucaptcha_key=self.RUCAPTCHA_KEY) as instance:
            assert instance.reportCorrect(id=random.randint(20, 50))

    @pytest.mark.asyncio
    async def test_aio_report_good(self):
        instance = Control(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = await instance.aio_reportCorrect(id=random.randint(20, 50))

        assert isinstance(result, dict) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_context_report_good(self):
        async with Control(rucaptcha_key=self.RUCAPTCHA_KEY) as instance:
            assert await instance.aio_reportCorrect(id=random.randint(20, 50))
