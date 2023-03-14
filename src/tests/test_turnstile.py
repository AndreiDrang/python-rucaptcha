import pytest

from tests.conftest import BaseTest
from python_rucaptcha.turnstile import Turnstile
from python_rucaptcha.core.enums import TurnstileCaptchaEnm
from python_rucaptcha.core.serializer import ResponseSer


class TestTurnstile(BaseTest):
    pageurl = "https://www.geetest.com/en/demo"
    sitekey = "0x4AAAAAAAC3DHQFLr1GavRN"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in Turnstile.__dict__.keys()
        assert "aio_captcha_handler" in Turnstile.__dict__.keys()

    def test_basic_data(self):
        instance = Turnstile(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            sitekey=self.sitekey,
            method=TurnstileCaptchaEnm.TURNSTILE.value,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == TurnstileCaptchaEnm.TURNSTILE.value
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
        instance = Turnstile(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            sitekey=self.sitekey,
            method=TurnstileCaptchaEnm.TURNSTILE.value,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == TurnstileCaptchaEnm.TURNSTILE.value
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
        with Turnstile(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            sitekey=self.sitekey,
            method=TurnstileCaptchaEnm.TURNSTILE.value,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == TurnstileCaptchaEnm.TURNSTILE.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["sitekey"] == self.sitekey

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with Turnstile(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            sitekey=self.sitekey,
            method=TurnstileCaptchaEnm.TURNSTILE.value,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == TurnstileCaptchaEnm.TURNSTILE.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["sitekey"] == self.sitekey

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            Turnstile(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                sitekey=self.sitekey,
                method=self.get_random_string(5),
            )
