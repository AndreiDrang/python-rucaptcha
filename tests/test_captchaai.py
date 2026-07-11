from unittest.mock import AsyncMock

import pytest

from python_rucaptcha.core import captchaai
from python_rucaptcha.captchaai import CaptchaAI, CaptchaAIFile
from python_rucaptcha.core.enums import ServiceEnm, ReCaptchaEnm
from python_rucaptcha.re_captcha import ReCaptcha
from python_rucaptcha.core.serializer import CaptchaOptionsSer, GetTaskResultResponseSer


class SyncResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class SyncSession:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return next(self.responses)


class AsyncResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    async def json(self, **kwargs):
        return self.payload


class AsyncRequest:
    def __init__(self, response):
        self.response = response

    async def __aenter__(self):
        return self.response

    async def __aexit__(self, *args):
        return None


class AsyncSession:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return AsyncRequest(next(self.responses))


def fields(call):
    return {name: value[1] for name, value in call[1]["files"].items() if value[0] is None}


class TestCaptchaAIService:
    """No-network coverage for native and legacy CaptchaAI API paths."""

    def test_service_urls(self):
        options = CaptchaOptionsSer(service_type=ServiceEnm.CAPTCHAAI)
        options.urls_set()
        assert options.url_request == "https://ocr.captchaai.com/in.php"
        assert options.url_response == "https://ocr.captchaai.com/res.php"

    def test_solution_supports_structured_provider_results(self):
        result = GetTaskResultResponseSer(solution={"click": [1, 3, 6]}).to_dict()
        assert result["solution"] == {"click": [1, 3, 6]}

    def test_profiles_cover_all_supplied_solver_contracts(self):
        expected = {
            "bls",
            "captchafox",
            "cloudflare-challenge",
            "friendly-captcha",
            "geetest-v3",
            "grid-base64",
            "grid-file",
            "lemin",
            "normal-base64",
            "normal-file",
            "normal-solve-base64",
            "normal-solve-file",
            "recaptcha-v2",
            "recaptcha-v2-enterprise",
            "recaptcha-v2-invisible",
            "recaptcha-v3",
            "recaptcha-v3-enterprise",
            "turnstile",
        }
        assert expected == set(CaptchaAI.profiles())

    @pytest.mark.parametrize(
        ("profile", "method"),
        [
            ("bls", "bls"),
            ("captchafox", "captchafox"),
            ("cloudflare-challenge", "cloudflare_challenge"),
            ("friendly-captcha", "friendly_captcha"),
            ("geetest-v3", "geetest"),
            ("lemin", "lemin"),
            ("recaptcha-v2", "userrecaptcha"),
            ("recaptcha-v3-enterprise", "userrecaptcha"),
            ("turnstile", "turnstile"),
        ],
    )
    def test_profile_methods_are_declarative(self, profile, method):
        assert captchaai.profile_method(profile) == method

    def test_unknown_future_method_is_passed_through(self, monkeypatch):
        session = SyncSession(
            [
                SyncResponse({"status": 1, "request": "FUTURE-1"}),
                SyncResponse({"status": 1, "request": "future-result"}),
            ]
        )
        monkeypatch.setattr(captchaai.time, "sleep", lambda _: None)

        result = captchaai.solve_native(
            key="api-key",
            method="provider_future_method",
            params={"custom_field": "custom-value"},
            url_request="submit-url",
            url_response="result-url",
            sleep_time=0,
            session=session,
        )

        assert result["taskId"] == "FUTURE-1"
        assert result["solution"] == {"request": "future-result"}
        assert fields(session.calls[0]) == {
            "key": "api-key",
            "method": "provider_future_method",
            "json": "1",
            "custom_field": "custom-value",
        }
        assert fields(session.calls[1]) == {"key": "api-key", "action": "get", "id": "FUTURE-1", "json": "1"}
        assert all(call[1]["timeout"] == captchaai.REQUEST_TIMEOUT for call in session.calls)

    def test_profile_defaults_and_enterprise_result_shape(self, monkeypatch):
        session = SyncSession(
            [
                SyncResponse({"status": 1, "request": "TASK-1"}),
                SyncResponse({"status": 1, "result": "enterprise-token", "user_agent": "UA"}),
            ]
        )
        monkeypatch.setattr(captchaai.time, "sleep", lambda _: None)

        result = captchaai.solve_native(
            key="api-key",
            method="userrecaptcha",
            params={"googlekey": "site-key", "pageurl": "https://example.com"},
            profile="recaptcha-v2-enterprise",
            url_request="submit-url",
            url_response="result-url",
            sleep_time=0,
            session=session,
        )

        assert fields(session.calls[0])["enterprise"] == "1"
        assert result["solution"]["token"] == "enterprise-token"
        assert result["solution"]["gRecaptchaResponse"] == "enterprise-token"
        assert result["solution"]["user_agent"] == "UA"

    def test_geetest_structured_response_without_status(self, monkeypatch):
        session = SyncSession(
            [
                SyncResponse({"status": 1, "request": "TASK-1"}),
                SyncResponse({"challenge": "challenge", "validate": "validate", "seccode": "seccode"}),
            ]
        )
        monkeypatch.setattr(captchaai.time, "sleep", lambda _: None)

        result = captchaai.solve_native(
            key="api-key",
            method="geetest",
            params={"gt": "gt", "challenge": "challenge", "pageurl": "https://example.com"},
            profile="geetest-v3",
            url_request="submit-url",
            url_response="result-url",
            sleep_time=0,
            session=session,
        )

        assert result["solution"] == {"challenge": "challenge", "validate": "validate", "seccode": "seccode"}

    def test_normal_file_direct_mode_uses_solve_endpoint(self):
        session = SyncSession([SyncResponse({"status": 1, "request": "captcha-text"})])
        captcha_file = CaptchaAIFile(b"png", filename="captcha.png", content_type="image/png")

        result = captchaai.solve_native(
            key="api-key",
            method="post",
            params={},
            files={"file": captcha_file},
            profile="normal-solve-file",
            url_request="https://ocr.captchaai.com/in.php",
            url_response="https://ocr.captchaai.com/res.php",
            sleep_time=0,
            session=session,
        )

        assert session.calls[0][0] == "https://ocr.captchaai.com/solve.php"
        assert session.calls[0][1]["files"]["file"] == ("captcha.png", b"png", "image/png")
        assert result["taskId"] is None
        assert result["solution"]["text"] == "captcha-text"

    def test_profile_rejects_missing_required_fields(self):
        result = captchaai.solve_native(
            key="api-key",
            method="cloudflare_challenge",
            params={"pageurl": "https://example.com"},
            profile="cloudflare-challenge",
            url_request="submit-url",
            url_response="result-url",
            sleep_time=0,
        )
        assert result["errorId"] == 12
        assert "proxy" in result["errorCode"]

    def test_file_profile_requires_a_file_part(self):
        result = captchaai.solve_native(
            key="api-key",
            method="post",
            params={"file": "not-a-binary-part"},
            profile="normal-file",
            url_request="submit-url",
            url_response="result-url",
            sleep_time=0,
        )
        assert result["errorId"] == 12
        assert "file" in result["errorCode"]

    def test_legacy_class_translation_uses_metadata_and_preserves_string_id(self, monkeypatch):
        session = SyncSession(
            [
                SyncResponse({"status": 1, "request": "ABC123"}),
                SyncResponse({"status": 1, "request": "captcha-token"}),
            ]
        )
        monkeypatch.setattr(captchaai.time, "sleep", lambda _: None)
        payload = {
            "clientKey": "api-key",
            "task": {
                "type": "RecaptchaV2Task",
                "websiteURL": "https://example.com",
                "websiteKey": "site-key",
                "proxyType": "HTTPS",
                "proxyAddress": "203.0.113.7",
                "proxyPort": 3128,
            },
        }

        result = captchaai.solve(payload, "submit-url", "result-url", sleep_time=0, session=session)

        assert result["taskId"] == "ABC123"
        assert result["solution"]["token"] == "captcha-token"
        submit = fields(session.calls[0])
        assert submit["method"] == "userrecaptcha"
        assert submit["googlekey"] == "site-key"
        assert submit["pageurl"] == "https://example.com"
        assert submit["proxy"] == "203.0.113.7:3128"
        assert submit["proxytype"] == "HTTPS"

    def test_high_level_v3_enterprise_uses_declarative_compatibility_profile(self, monkeypatch):
        captured = {}

        def solve(**kwargs):
            captured.update(kwargs)
            return {"errorId": 0}

        monkeypatch.setattr(captchaai, "solve", solve)
        instance = ReCaptcha(
            rucaptcha_key="api-key",
            service_type=ServiceEnm.CAPTCHAAI,
            websiteURL="https://example.com",
            websiteKey="site-key",
            method=ReCaptchaEnm.RecaptchaV3EnterpriseTaskProxyless,
        )

        assert instance.captcha_handler() == {"errorId": 0}
        assert captured["session"] is instance.session

    def test_control_operations_are_declarative(self):
        session = SyncSession([SyncResponse({"status": 1, "request": "600"})])
        result = captchaai.control("api-key", "balance", "result-url", session=session)

        assert result == {"request": "600", "balance": "600"}
        assert fields(session.calls[0]) == {"key": "api-key", "json": "1", "action": "getbalance"}

    def test_invalid_response_is_reported(self):
        session = SyncSession([SyncResponse([])])
        result = captchaai.solve_native(
            key="api-key",
            method="future",
            params={},
            url_request="submit-url",
            url_response="result-url",
            sleep_time=0,
            session=session,
        )
        assert result["errorId"] == 12
        assert result["errorCode"].startswith("ERROR_SUBMIT")

    async def test_async_native_future_method(self, monkeypatch):
        session = AsyncSession(
            [
                AsyncResponse({"status": 1, "request": "ABC123"}),
                AsyncResponse({"status": 0, "request": "CAPCHA_NOT_READY"}),
                AsyncResponse({"status": 1, "request": "captcha-token"}),
            ]
        )
        monkeypatch.setattr(captchaai.aiohttp, "ClientSession", lambda **kwargs: session)
        monkeypatch.setattr(captchaai, "_aio_form", lambda values, files: dict(values))
        monkeypatch.setattr(captchaai.asyncio, "sleep", AsyncMock())

        result = await captchaai.aio_solve_native(
            key="api-key",
            method="future_method",
            params={"provider_option": "enabled"},
            url_request="submit-url",
            url_response="result-url",
            sleep_time=0,
        )

        assert result["taskId"] == "ABC123"
        assert result["solution"] == {"request": "captcha-token"}
        assert [call[0] for call in session.calls] == ["submit-url", "result-url", "result-url"]
        assert session.calls[0][1]["data"] == {
            "key": "api-key",
            "method": "future_method",
            "json": 1,
            "provider_option": "enabled",
        }

    def test_aio_form_is_multipart_for_scalar_and_file_fields(self):
        form = captchaai._aio_form({"key": "api-key"}, {"file": CaptchaAIFile(b"image")})
        assert form.is_multipart

    def test_public_client_requires_method_or_profile(self):
        with pytest.raises(ValueError):
            CaptchaAI(rucaptcha_key="api-key")

    def test_public_client_dispatches_native_method(self, monkeypatch):
        captured = {}

        def solve_native(**kwargs):
            captured.update(kwargs)
            return {"errorId": 0}

        monkeypatch.setattr(captchaai, "solve_native", solve_native)
        client = CaptchaAI(
            rucaptcha_key="api-key",
            method="provider_future_method",
            params={"provider_field": "value"},
        )

        assert client.captcha_handler() == {"errorId": 0}
        assert captured["method"] == "provider_future_method"
        assert captured["params"] == {"provider_field": "value"}
        assert captured["session"] is client.session
