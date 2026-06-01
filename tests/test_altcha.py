import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import AltchaEnm
from python_rucaptcha.altcha_captcha import AltchaCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestAltcha(BaseTest):
    pageurl = "https://example.com"
    challenge_url = "https://example.com/altcha/challenge.js"
    challenge_json = '{"challenge":"test_data"}'
    useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    kwargs_params = {
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }

    def test_methods_exists(self):
        assert "captcha_handler" in AltchaCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in AltchaCaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", AltchaEnm.list_values())
    def test_args(self, method: str):
        kwargs = {}
        if method == AltchaEnm.AltchaTask.value:
            kwargs = {"proxyType": "http", "proxyAddress": "1.2.3.4", "proxyPort": 8080}
        instance = AltchaCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            challengeURL=self.challenge_url,
            userAgent=self.useragent,
            method=method,
            **kwargs,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.pageurl
        assert instance.create_task_payload["task"]["challengeURL"] == self.challenge_url

    def test_kwargs(self):
        instance = AltchaCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            challengeURL=self.challenge_url,
            method=AltchaEnm.AltchaTask,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    def test_xor_validation_both_params(self):
        """Test that providing both challengeURL and challengeJSON raises ValueError"""
        with pytest.raises(ValueError, match="challengeURL|challengeJSON"):
            AltchaCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                challengeURL=self.challenge_url,
                challengeJSON=self.challenge_json,
                method=AltchaEnm.AltchaTaskProxyless,
            )

    def test_xor_validation_neither_param(self):
        """Test that providing neither challengeURL nor challengeJSON raises ValueError"""
        with pytest.raises(ValueError, match="challengeURL|challengeJSON"):
            AltchaCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                method=AltchaEnm.AltchaTaskProxyless,
            )

    def test_valid_challenge_url(self):
        """Test that providing only challengeURL works correctly"""
        instance = AltchaCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            challengeURL=self.challenge_url,
            method=AltchaEnm.AltchaTaskProxyless,
        )
        assert instance.create_task_payload["task"]["challengeURL"] == self.challenge_url
        assert "challengeJSON" not in instance.create_task_payload["task"]

    def test_valid_challenge_json(self):
        """Test that providing only challengeJSON works correctly"""
        instance = AltchaCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            challengeJSON=self.challenge_json,
            method=AltchaEnm.AltchaTaskProxyless,
        )
        assert instance.create_task_payload["task"]["challengeJSON"] == self.challenge_json
        assert "challengeURL" not in instance.create_task_payload["task"]

    def test_proxy_params_in_payload(self):
        """Test that proxy params are included in payload for AltchaTask method"""
        instance = AltchaCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            challengeURL=self.challenge_url,
            method=AltchaEnm.AltchaTask,
            proxyType="http",
            proxyAddress="1.2.3.4",
            proxyPort=8080,
        )
        assert instance.create_task_payload["task"]["proxyType"] == "http"
        assert instance.create_task_payload["task"]["proxyAddress"] == "1.2.3.4"
        assert instance.create_task_payload["task"]["proxyPort"] == 8080

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            AltchaCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                challengeURL=self.challenge_url,
                method=self.get_random_string(5),
            )

    """
    Success tests
    """

    def test_basic_data(self):
        instance = AltchaCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            challengeURL=self.challenge_url,
            method=AltchaEnm.AltchaTaskProxyless.value,
        )

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"], dict) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    async def test_aio_basic_data(self):
        instance = AltchaCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            challengeURL=self.challenge_url,
            method=AltchaEnm.AltchaTaskProxyless.value,
        )

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"], dict) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with AltchaCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            challengeURL=self.challenge_url,
            method=AltchaEnm.AltchaTaskProxyless.value,
        ) as instance:
            assert instance

    async def test_context_aio_basic_data(self):
        async with AltchaCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            challengeURL=self.challenge_url,
            method=AltchaEnm.AltchaTaskProxyless.value,
        ) as instance:
            assert instance

    """
    Fail tests
    """
