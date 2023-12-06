import pytest

from tests.conftest import BaseTest
from python_rucaptcha.amazon_waf import AmazonWAF
from python_rucaptcha.core.enums import AmazonWAFCaptchaEnm


class TestAmazonCaptcha(BaseTest):
    pageurl = "https://captcha-api.yandex.ru/demo"
    sitekey = "FEXfAbHQsToo97VidNVk3j4dC74nGW1DgdxjtNB9"
    iv = "some-iv-value"
    context = "some-context-value"

    @pytest.mark.parametrize("method", AmazonWAFCaptchaEnm.list_values())
    def test_args(self, method: str):
        instance = AmazonWAF(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            iv=self.iv,
            context=self.context,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["websiteURL"] == self.pageurl
        assert instance.create_task_payload["task"]["websiteKey"] == self.sitekey
        assert instance.create_task_payload["task"]["iv"] == self.iv
        assert instance.create_task_payload["task"]["context"] == self.context
        assert instance.create_task_payload["task"]["type"] == method

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in AmazonWAF.__dict__.keys()
        assert "aio_captcha_handler" in AmazonWAF.__dict__.keys()

    def test_basic_data(self):
        instance = AmazonWAF(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            iv=self.iv,
            context=self.context,
            method=AmazonWAFCaptchaEnm.AmazonTaskProxyless.value,
        )
        assert instance.captcha_handler()

    def test_context_basic_data(self):
        with AmazonWAF(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            iv=self.iv,
            context=self.context,
            method=AmazonWAFCaptchaEnm.AmazonTaskProxyless.value,
        ) as instance:
            assert instance.captcha_handler()

    async def test_aio_basic_data(self):
        instance = AmazonWAF(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            iv=self.iv,
            context=self.context,
            method=AmazonWAFCaptchaEnm.AmazonTaskProxyless.value,
        )
        assert await instance.aio_captcha_handler()

    async def test_aio_context_basic_data(self):
        async with AmazonWAF(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            iv=self.iv,
            context=self.context,
            method=AmazonWAFCaptchaEnm.AmazonTaskProxyless.value,
        ) as instance:
            assert await instance.aio_captcha_handler()

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            AmazonWAF(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                websiteKey=self.sitekey,
                iv=self.iv,
                context=self.context,
                method=self.get_random_string(5),
            )
