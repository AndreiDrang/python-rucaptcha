import logging

import pytest

from .conftest import CoreTest
from ..python_rucaptcha.enums import GeetestEnm
from ..python_rucaptcha.GeeTest import GeeTest, aioGeeTest
from ..python_rucaptcha.serializer import ResponseSer


class TestGeetest(CoreTest):
    gt = "f1ab2cdefa3456789012345b6c78d90e"
    pageurl = "https://www.site.com/page/"
    api_server = "api-na.geetest.com"
    challenge = "12345678abc90123d45678ef90123a456b"
    captcha_id = "f1ab2cdefa3456789012345b6c78d90e"

    """
    Success tests
    """

    @pytest.mark.parametrize("method", GeetestEnm.list_values())
    def test_geetest_basic_data(self, method):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            captcha_id=self.captcha_id,
            method=method,
            pageurl=self.pageurl,
            api_server=self.api_server,
        )
        assert instance.params.method == method
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["gt"] == self.gt
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["api_server"] == self.api_server
        assert instance.post_payload["captcha_id"] == self.captcha_id

        result = instance.captcha_handler(challenge=self.challenge)

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method", GeetestEnm.list_values())
    async def test_aio_geetest_basic_data(self, method):
        instance = aioGeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            captcha_id=self.captcha_id,
            method=method,
            pageurl=self.pageurl,
            api_server=self.api_server,
        )
        assert instance.params.method == method
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["gt"] == self.gt
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["api_server"] == self.api_server
        assert instance.post_payload["captcha_id"] == self.captcha_id

        result = await instance.captcha_handler(challenge=self.challenge)

        logging.warning(result)
        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result.keys() == ResponseSer().dict().keys()

    """
    Failed tests
    """

    def test_failed_geetest_method(self):
        with pytest.raises(ValueError):
            GeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                gt=self.gt,
                method=self.get_random_string(5),
                pageurl=self.pageurl,
                api_server=self.api_server,
            )

    def test_aio_failed_geetest_method(self):
        with pytest.raises(ValueError):
            aioGeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                gt=self.gt,
                method=self.get_random_string(5),
                pageurl=self.pageurl,
                api_server=self.api_server,
            )

    def test_failed_geetest_challenge(self):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GEETEST.value,
            pageurl=self.pageurl,
            api_server=self.api_server,
        )
        with pytest.raises(ValueError):
            instance.captcha_handler()

    @pytest.mark.asyncio
    async def test_aio_failed_geetest_challenge(self):
        instance = aioGeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GEETEST.value,
            pageurl=self.pageurl,
            api_server=self.api_server,
        )
        with pytest.raises(ValueError):
            await instance.captcha_handler()

    @pytest.mark.parametrize(
        "method_param", [[GeetestEnm.GEETEST.value, {"gt": None}], [GeetestEnm.GEETEST_V4.value, {"captcha_id": None}]]
    )
    def test_failed_geetest_method_params(self, method_param):
        with pytest.raises(ValueError):
            GeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                method=method_param[0],
                pageurl=self.pageurl,
                api_server=self.api_server,
                **method_param[1],
            )
