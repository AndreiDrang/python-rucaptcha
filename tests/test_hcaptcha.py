import pytest

from tests.conftest import BaseTest
from python_rucaptcha.hcaptcha import HCaptcha
from python_rucaptcha.core.enums import HCaptchaEnm
from python_rucaptcha.core.serializer import ResponseSer


class TestHCaptcha(BaseTest):
    sitekey = "3ceb8624-1970-4e6b-91d5-70317b70b651"
    pageurl = "https://rucaptcha.com/demo/hcaptcha"
    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in HCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in HCaptcha.__dict__.keys()

    def test_basic_data(self):
        instance = HCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            sitekey=self.sitekey,
            pageurl=self.pageurl,
            method=HCaptchaEnm.HCAPTCHA.value,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == HCaptchaEnm.HCAPTCHA.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["sitekey"] == self.sitekey

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = HCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            sitekey=self.sitekey,
            pageurl=self.pageurl,
            method=HCaptchaEnm.HCAPTCHA.value,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == HCaptchaEnm.HCAPTCHA.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["sitekey"] == self.sitekey

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == ResponseSer().dict().keys()

    def test_context_basic_data(self):
        with HCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            sitekey=self.sitekey,
            pageurl=self.pageurl,
            method=HCaptchaEnm.HCAPTCHA.value,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == HCaptchaEnm.HCAPTCHA.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["sitekey"] == self.sitekey

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with HCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            sitekey=self.sitekey,
            pageurl=self.pageurl,
            method=HCaptchaEnm.HCAPTCHA.value,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == HCaptchaEnm.HCAPTCHA.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["sitekey"] == self.sitekey

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            HCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                sitekey=self.sitekey,
                pageurl=self.pageurl,
                method=self.get_random_string(length=5),
            )
