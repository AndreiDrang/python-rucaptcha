import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import FunCaptchaEnm
from python_rucaptcha.fun_captcha import FunCaptcha
from python_rucaptcha.core.serializer import ResponseSer


class TestFunCaptcha(BaseTest):
    publickey = "69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC"
    pageurl = (
        "https://api.funcaptcha.com/tile-game-lite-mode/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC&lang=en"
    )
    surl = "https://client-api.arkoselabs.com"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in FunCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in FunCaptcha.__dict__.keys()

    def test_basic_data(self):
        instance = FunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            publickey=self.publickey,
            surl=self.surl,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == FunCaptchaEnm.FUNCAPTCHA.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["publickey"] == self.publickey
        assert instance.post_payload["surl"] == self.surl

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
        instance = FunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            publickey=self.publickey,
            surl=self.surl,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == FunCaptchaEnm.FUNCAPTCHA.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["publickey"] == self.publickey
        assert instance.post_payload["surl"] == self.surl

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
        with FunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            publickey=self.publickey,
            surl=self.surl,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == FunCaptchaEnm.FUNCAPTCHA.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["publickey"] == self.publickey
            assert instance.post_payload["surl"] == self.surl

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with FunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            publickey=self.publickey,
            surl=self.surl,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == FunCaptchaEnm.FUNCAPTCHA.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["publickey"] == self.publickey
            assert instance.post_payload["surl"] == self.surl

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            FunCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                publickey=self.publickey,
                surl=self.surl,
                method=self.get_random_string(length=5),
            )
