import pytest

from python_rucaptcha.core.enums import IncapsulaEnm
from python_rucaptcha.incapsula_captcha import ImpervaCaptcha, IncapsulaCaptcha

KEY = "test-key"


class TestIncapsulaCaptcha:
    def test_methods_exist(self):
        assert "captcha_handler" in IncapsulaCaptcha.__dict__
        assert "aio_captcha_handler" in IncapsulaCaptcha.__dict__

    def test_payload(self):
        instance = IncapsulaCaptcha(
            rucaptcha_key=KEY,
            websiteURL="https://example.com",
            incapsulaScriptUrl="_Incapsula_Resource?SWJIYLWA=example",
            incapsulaCookies="incap_sess_abc=value; visid_incap_abc=value",
            proxyType="http",
            proxyAddress="203.0.113.10",
            proxyPort=8080,
            userAgent="Mozilla/5.0",
            reese84UrlEndpoint="https://example.com/?d=example.com",
            proxyLogin="user",
            proxyPassword="password",
        )
        task = instance.create_task_payload["task"]

        assert task["type"] == IncapsulaEnm.IncapsulaTask.value
        assert task["incapsulaScriptUrl"].startswith("_Incapsula_Resource")
        assert task["incapsulaCookies"].startswith("incap_sess_")
        assert task["reese84UrlEndpoint"] == "https://example.com/?d=example.com"
        assert task["proxyLogin"] == "user"
        assert task["proxyPassword"] == "password"

    def test_alias(self):
        assert ImpervaCaptcha is IncapsulaCaptcha

    def test_invalid_method(self):
        with pytest.raises(ValueError):
            IncapsulaCaptcha(
                rucaptcha_key=KEY,
                websiteURL="https://example.com",
                incapsulaScriptUrl="script",
                incapsulaCookies="cookies",
                proxyType="http",
                proxyAddress="203.0.113.10",
                proxyPort=8080,
                method="invalid",
            )

    def test_required_arguments(self):
        with pytest.raises(TypeError):
            IncapsulaCaptcha(
                rucaptcha_key=KEY,
                websiteURL="https://example.com",
                incapsulaScriptUrl="script",
                incapsulaCookies="cookies",
                proxyType="http",
                proxyAddress="203.0.113.10",
            )
