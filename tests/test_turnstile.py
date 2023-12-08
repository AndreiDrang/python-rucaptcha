import pytest

from tests.conftest import BaseTest
from python_rucaptcha.turnstile import Turnstile
from python_rucaptcha.core.enums import TurnstileCaptchaEnm
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestTurnstile(BaseTest):
    pageurl = "https://rucaptcha.com/demo/cloudflare-turnstile"
    sitekey = "0x4AAAAAAAC3DHQFLr1GavRN"
    useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    kwargs_params = {
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }

    def test_methods_exists(self):
        assert "captcha_handler" in Turnstile.__dict__.keys()
        assert "aio_captcha_handler" in Turnstile.__dict__.keys()

    @pytest.mark.parametrize("method", TurnstileCaptchaEnm.list_values())
    def test_args(self, method: str):
        instance = Turnstile(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            userAgent=self.useragent,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.pageurl
        assert instance.create_task_payload["task"]["websiteKey"] == self.sitekey
        assert instance.create_task_payload["task"]["userAgent"] == self.useragent

    def test_kwargs(self):
        instance = Turnstile(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            userAgent=self.useragent,
            method=TurnstileCaptchaEnm.TurnstileTaskProxyless,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    """
    Success tests
    """

    def test_basic_data(self):
        instance = Turnstile(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            userAgent=self.useragent,
            method=TurnstileCaptchaEnm.TurnstileTaskProxyless.value,
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
        instance = Turnstile(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            userAgent=self.useragent,
            method=TurnstileCaptchaEnm.TurnstileTaskProxyless.value,
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
        with Turnstile(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            userAgent=self.useragent,
            method=TurnstileCaptchaEnm.TurnstileTaskProxyless.value,
        ) as instance:
            assert instance.captcha_handler()

    async def test_context_aio_basic_data(self):
        async with Turnstile(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            userAgent=self.useragent,
            method=TurnstileCaptchaEnm.TurnstileTaskProxyless.value,
        ) as instance:
            assert await instance.aio_captcha_handler()

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            Turnstile(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                websiteKey=self.sitekey,
                userAgent=self.useragent,
                method=self.get_random_string(5),
            )
