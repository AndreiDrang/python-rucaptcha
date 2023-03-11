import pytest
from tenacity import AsyncRetrying
from urllib3.util.retry import Retry

from src.tests.conftest import BaseTest
from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import MyEnum, GeetestEnm
from python_rucaptcha.core.config import RETRIES, ASYNC_RETRIES, attempts_generator


class TestMain(BaseTest):
    """
    Success tests
    """

    def test_reties(self):
        assert isinstance(RETRIES, Retry)

    def test_async_reties(self):
        assert isinstance(ASYNC_RETRIES, AsyncRetrying)

    def test_context_class_create(self):
        with BaseCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, method=GeetestEnm.GEETEST.value) as bc:
            pass

    def test_class_create(self):
        bc = BaseCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, method=GeetestEnm.GEETEST.value)

    @pytest.mark.asyncio
    async def test_aio_context_class_create(self):
        async with BaseCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, method=GeetestEnm.GEETEST.value) as bc:
            pass

    """
    Failed tests
    """

    @pytest.mark.parametrize("elements", [31, 33])
    def test_context_failed_api_key(self, elements):
        with pytest.raises(ValueError):
            with BaseCaptcha(rucaptcha_key=self.get_random_string(elements), method=GeetestEnm.GEETEST.value):
                pass

    @pytest.mark.parametrize("elements", [31, 33])
    def test_failed_api_key(self, elements):
        with pytest.raises(ValueError):
            BaseCaptcha(rucaptcha_key=self.get_random_string(elements), method=GeetestEnm.GEETEST.value)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("elements", [31, 33])
    async def test_aio_context_failed_api_key(self, elements):
        with pytest.raises(ValueError):
            async with BaseCaptcha(rucaptcha_key=self.get_random_string(elements), method=GeetestEnm.GEETEST.value):
                pass

    def test_failed_service(self):
        with pytest.raises(ValueError):
            bc = BaseCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                method=GeetestEnm.GEETEST.value,
                service_type=self.get_random_string(length=10),
            )

    def test_context_failed_service(self):
        with pytest.raises(ValueError):
            with BaseCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                method=GeetestEnm.GEETEST.value,
                service_type=self.get_random_string(length=10),
            ) as bc:
                pass


class TestEnum(BaseTest):
    def test_enum_list(self):
        assert isinstance(MyEnum.list(), list)

    def test_enum_list_values(self):
        assert isinstance(MyEnum.list_values(), list)

    def test_enum_list_names(self):
        assert isinstance(MyEnum.list_names(), list)


class TestConfig(BaseTest):
    def test_attempts_generator(self):
        attempt = None
        attempts = attempts_generator(amount=5)
        for attempt in attempts:
            assert isinstance(attempt, int)
        assert attempt == 4
