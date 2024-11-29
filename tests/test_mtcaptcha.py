import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import MTCaptchaEnm
from python_rucaptcha.mt_captcha import MTCaptcha


class TestMTCaptcha(BaseTest):
    websiteURL = "https://service.mtcaptcha.com/mtcv1/demo/index.html"
    websiteKey = "MTPublic-DemoKey9M"

    kwargs_params = {
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }

    def test_methods_exists(self):
        assert "captcha_handler" in MTCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in MTCaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", MTCaptchaEnm.list_values())
    def test_args(self, method: str):
        instance = MTCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.websiteURL
        assert instance.create_task_payload["task"]["websiteKey"] == self.websiteKey

    def test_kwargs(self):
        instance = MTCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    """
    Fail tests
    """

    def test_no_websiteURL(self):
        with pytest.raises(TypeError):
            MTCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteKey=self.websiteKey,
            )

    def test_no_websiteKey(self):
        with pytest.raises(TypeError):
            MTCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
            )

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            MTCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                websiteKey=self.websiteKey,
                method=self.get_random_string(length=5),
            )
