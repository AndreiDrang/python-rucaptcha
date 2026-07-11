import pytest

from python_rucaptcha.core import captchaai
from python_rucaptcha.core.enums import ServiceEnm
from python_rucaptcha.core.serializer import CaptchaOptionsSer


class TestCaptchaAIService:
    """Unit tests for the CaptchaAI classic-API provider adapter (no network)."""

    def test_service_enum(self):
        assert ServiceEnm.CAPTCHAAI.value == "captchaai"
        assert "captchaai" in ServiceEnm.list_values()

    def test_urls_set(self):
        opts = CaptchaOptionsSer(service_type=ServiceEnm.CAPTCHAAI)
        opts.urls_set()
        assert opts.url_request == "https://ocr.captchaai.com/in.php"
        assert opts.url_response == "https://ocr.captchaai.com/res.php"

    def test_map_turnstile(self):
        method, extra = captchaai.build_classic_params(
            {"type": "TurnstileTaskProxyless", "websiteKey": "0xAAA", "websiteURL": "https://x.com"}
        )
        assert method == "turnstile"
        assert extra == {"sitekey": "0xAAA", "pageurl": "https://x.com"}

    def test_map_recaptcha_v2(self):
        method, extra = captchaai.build_classic_params(
            {"type": "RecaptchaV2TaskProxyless", "websiteKey": "k", "websiteURL": "https://x"}
        )
        assert method == "userrecaptcha"
        assert extra["googlekey"] == "k"
        assert extra["pageurl"] == "https://x"

    def test_map_recaptcha_v2_enterprise(self):
        method, extra = captchaai.build_classic_params(
            {"type": "RecaptchaV2EnterpriseTaskProxyless", "websiteKey": "k", "websiteURL": "https://x"}
        )
        assert method == "userrecaptcha"
        assert extra["enterprise"] == 1

    def test_map_recaptcha_v3(self):
        method, extra = captchaai.build_classic_params(
            {
                "type": "RecaptchaV3TaskProxyless",
                "websiteKey": "k",
                "websiteURL": "https://x",
                "pageAction": "login",
                "minScore": 0.7,
            }
        )
        assert method == "userrecaptcha"
        assert extra["version"] == "v3"
        assert extra["action"] == "login"
        assert extra["min_score"] == 0.7

    def test_map_image(self):
        method, extra = captchaai.build_classic_params({"type": "ImageToTextTask", "body": "B64"})
        assert method == "base64"
        assert extra == {"body": "B64"}

    def test_unsupported_type_raises(self):
        with pytest.raises(ValueError):
            captchaai.build_classic_params(
                {"type": "HCaptchaTaskProxyless", "websiteKey": "k", "websiteURL": "u"}
            )

    def test_solution_shapes(self):
        assert captchaai._solution("base64", "abc") == {"text": "abc"}
        token = captchaai._solution("turnstile", "tok")
        assert token["token"] == "tok"
        assert token["gRecaptchaResponse"] == "tok"
