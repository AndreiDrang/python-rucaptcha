import pytest

from .conftest import CoreTest
from ..python_rucaptcha.base import BaseCaptcha
from ..python_rucaptcha.enums import GeetestEnm


class TestMain(CoreTest):
    """
    Success tests
    """

    def test_context_class_create(self):
        with BaseCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, method=GeetestEnm.GEETEST.value) as bc:
            pass

    def test_class_create(self):
        bc = BaseCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, method=GeetestEnm.GEETEST.value)

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
