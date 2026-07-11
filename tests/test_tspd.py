import pytest

from python_rucaptcha.core.enums import TSPDEnm
from python_rucaptcha.tspd_captcha import TSPDCaptcha

KEY = "test-key"


class TestTSPDCaptcha:
    def test_methods_exist(self):
        assert "captcha_handler" in TSPDCaptcha.__dict__
        assert "aio_captcha_handler" in TSPDCaptcha.__dict__

    def test_payload(self):
        instance = TSPDCaptcha(
            rucaptcha_key=KEY,
            websiteURL="https://example.com",
            tspdcookie="TS386a=challenge-cookie",
            htmlPageBase64="PGh0bWw+Y2hhbGxlbmdlPC9odG1sPg==",
            proxyType="http",
            proxyAddress="203.0.113.10",
            proxyPort=8080,
            userAgent="Mozilla/5.0",
            proxyLogin="user",
            proxyPassword="password",
        )
        task = instance.create_task_payload["task"]

        assert task["type"] == TSPDEnm.TspdTask.value
        assert task["websiteURL"] == "https://example.com"
        assert task["tspdcookie"] == "TS386a=challenge-cookie"
        assert task["htmlPageBase64"] == "PGh0bWw+Y2hhbGxlbmdlPC9odG1sPg=="
        assert task["proxyPort"] == 8080
        assert task["userAgent"] == "Mozilla/5.0"
        assert task["proxyLogin"] == "user"
        assert task["proxyPassword"] == "password"

    def test_invalid_method(self):
        with pytest.raises(ValueError):
            TSPDCaptcha(
                rucaptcha_key=KEY,
                websiteURL="https://example.com",
                tspdcookie="cookie",
                htmlPageBase64="html",
                proxyType="http",
                proxyAddress="203.0.113.10",
                proxyPort=8080,
                method="invalid",
            )

    def test_required_arguments(self):
        with pytest.raises(TypeError):
            TSPDCaptcha(
                rucaptcha_key=KEY,
                websiteURL="https://example.com",
                tspdcookie="cookie",
                htmlPageBase64="html",
                proxyType="http",
                proxyAddress="203.0.113.10",
            )
