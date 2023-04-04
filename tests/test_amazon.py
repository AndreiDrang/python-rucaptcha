import pytest

from tests.conftest import BaseTest
from python_rucaptcha.amazon_waf import AmazonWAF
from python_rucaptcha.core.enums import AmazonWAFCaptchaEnm


class TestAmazonCaptcha(BaseTest):
    pageurl = "https://captcha-api.yandex.ru/demo"
    sitekey = "FEXfAbHQsToo97VidNVk3j4dC74nGW1DgdxjtNB9"
    iv = "some-iv-value"
    context = "some-context-value"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in AmazonWAF.__dict__.keys()
        assert "aio_captcha_handler" in AmazonWAF.__dict__.keys()

    def test_basic_data(self):
        instance = AmazonWAF(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            sitekey=self.sitekey,
            iv=self.iv,
            context=self.context,
            method=AmazonWAFCaptchaEnm.AMAZON_WAF.value,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == AmazonWAFCaptchaEnm.AMAZON_WAF.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["sitekey"] == self.sitekey
        assert instance.post_payload["iv"] == self.iv
        assert instance.post_payload["context"] == self.context

    def test_context_basic_data(self):
        with AmazonWAF(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            sitekey=self.sitekey,
            iv=self.iv,
            context=self.context,
            method=AmazonWAFCaptchaEnm.AMAZON_WAF.value,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == AmazonWAFCaptchaEnm.AMAZON_WAF.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["sitekey"] == self.sitekey
            assert instance.post_payload["iv"] == self.iv
            assert instance.post_payload["context"] == self.context

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            AmazonWAF(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                sitekey=self.sitekey,
                iv=self.iv,
                context=self.context,
                method=self.get_random_string(5),
            )
