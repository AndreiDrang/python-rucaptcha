import pytest

from python_rucaptcha.core.enums import BasiliskEnm
from python_rucaptcha.basilisk_captcha import BasiliskCaptcha

KEY = "test-key"


class TestBasiliskCaptcha:
    def test_methods_exist(self):
        assert "captcha_handler" in BasiliskCaptcha.__dict__
        assert "aio_captcha_handler" in BasiliskCaptcha.__dict__

    @pytest.mark.parametrize("method", BasiliskEnm.list_values())
    def test_payload(self, method):
        proxy = {}
        if method == BasiliskEnm.BasiliskTask.value:
            proxy = {"proxyType": "http", "proxyAddress": "203.0.113.10", "proxyPort": 8080}

        instance = BasiliskCaptcha(
            rucaptcha_key=KEY,
            websiteURL="https://example.com",
            websiteKey="site-key",
            method=method,
            userAgent="Mozilla/5.0",
            **proxy,
        )
        task = instance.create_task_payload["task"]

        assert task["type"] == method
        assert task["websiteURL"] == "https://example.com"
        assert task["websiteKey"] == "site-key"
        assert task["userAgent"] == "Mozilla/5.0"
        if method == BasiliskEnm.BasiliskTask.value:
            assert task["proxyAddress"] == "203.0.113.10"
        else:
            assert "proxyAddress" not in task

    def test_proxy_required(self):
        with pytest.raises(ValueError, match="proxyType|proxyAddress|proxyPort"):
            BasiliskCaptcha(
                rucaptcha_key=KEY,
                websiteURL="https://example.com",
                websiteKey="site-key",
                method=BasiliskEnm.BasiliskTask,
            )

    def test_invalid_method(self):
        with pytest.raises(ValueError):
            BasiliskCaptcha(
                rucaptcha_key=KEY,
                websiteURL="https://example.com",
                websiteKey="site-key",
                method="invalid",
            )
