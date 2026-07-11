import pytest

from python_rucaptcha.core.enums import AlibabaEnm
from python_rucaptcha.alibaba_captcha import AlibabaCaptcha

KEY = "test-key"


class TestAlibabaCaptcha:
    def test_methods_exist(self):
        assert "captcha_handler" in AlibabaCaptcha.__dict__
        assert "aio_captcha_handler" in AlibabaCaptcha.__dict__

    @pytest.mark.parametrize("method", AlibabaEnm.list_values())
    def test_payload(self, method):
        proxy = {}
        if method == AlibabaEnm.AlibabaTask.value:
            proxy = {"proxyType": "socks5", "proxyAddress": "203.0.113.10", "proxyPort": 1080}

        instance = AlibabaCaptcha(
            rucaptcha_key=KEY,
            websiteURL="https://example.com",
            sceneId="scene-123",
            prefix="captcha-prefix",
            method=method,
            userId="user-123",
            userUserId="secondary-user",
            verifyType="verify",
            region="cn",
            userCertifyId="certify-123",
            apiGetLib="https://example.com/captcha.js",
            userAgent="Mozilla/5.0",
            **proxy,
        )
        task = instance.create_task_payload["task"]

        assert task["type"] == method
        assert task["sceneId"] == "scene-123"
        assert task["prefix"] == "captcha-prefix"
        assert task["userCertifyId"] == "certify-123"
        assert task["apiGetLib"] == "https://example.com/captcha.js"
        if method == AlibabaEnm.AlibabaTask.value:
            assert task["proxyPort"] == 1080
        else:
            assert "proxyPort" not in task

    def test_proxy_required(self):
        with pytest.raises(ValueError, match="proxyType|proxyAddress|proxyPort"):
            AlibabaCaptcha(
                rucaptcha_key=KEY,
                websiteURL="https://example.com",
                sceneId="scene-123",
                prefix="captcha-prefix",
                method=AlibabaEnm.AlibabaTask,
            )

    def test_invalid_method(self):
        with pytest.raises(ValueError):
            AlibabaCaptcha(
                rucaptcha_key=KEY,
                websiteURL="https://example.com",
                sceneId="scene-123",
                prefix="captcha-prefix",
                method="invalid",
            )
