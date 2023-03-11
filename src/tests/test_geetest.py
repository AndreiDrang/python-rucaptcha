import pytest

from src.tests.conftest import BaseTest
from python_rucaptcha.gee_test import GeeTest
from python_rucaptcha.core.enums import GeetestEnm
from python_rucaptcha.core.serializer import ResponseSer


class TestGeeTest(BaseTest):
    pageurl = "https://www.geetest.com/en/demo"
    challenge = "1ad03db8aff920037fb8117827eab171"
    gt = "022397c99c9f646f6477822485f30404"
    api_server = "api.geetest.com"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in GeeTest.__dict__.keys()
        assert "aio_captcha_handler" in GeeTest.__dict__.keys()

    def test_basic_data(self):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GEETEST.value,
            pageurl=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == GeetestEnm.GEETEST.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["api_server"] == self.api_server
        assert instance.post_payload["gt"] == self.gt
        assert instance.post_payload["new_captcha"] == 1

        result = instance.captcha_handler(challenge=self.challenge)

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert isinstance(result["errorBody"], str) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GEETEST.value,
            pageurl=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == GeetestEnm.GEETEST.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["api_server"] == self.api_server
        assert instance.post_payload["gt"] == self.gt
        assert instance.post_payload["new_captcha"] == 1

        result = await instance.aio_captcha_handler(challenge=self.challenge)

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert isinstance(result["errorBody"], str) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_basic_data(self):
        with GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GEETEST.value,
            pageurl=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == GeetestEnm.GEETEST.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["api_server"] == self.api_server
            assert instance.post_payload["gt"] == self.gt
            assert instance.post_payload["new_captcha"] == 1

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GEETEST.value,
            pageurl=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == GeetestEnm.GEETEST.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["api_server"] == self.api_server
            assert instance.post_payload["gt"] == self.gt
            assert instance.post_payload["new_captcha"] == 1

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            GeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                gt=self.gt,
                pageurl=self.pageurl,
                api_server=self.api_server,
                method=self.get_random_string(length=5),
            )

    def test_wrong_method_arg(self):
        with pytest.raises(ValueError):
            GeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                api_server=self.api_server,
                method=GeetestEnm.GEETEST.value,
            )
