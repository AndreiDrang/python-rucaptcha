import pytest

from tests.conftest import BaseTest
from python_rucaptcha.hcaptcha import HCaptcha
from python_rucaptcha.core.enums import HCaptchaEnm
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestHCaptcha(BaseTest):
    sitekey = "3ceb8624-1970-4e6b-91d5-70317b70b651"
    pageurl = "https://rucaptcha.com/demo/hcaptcha"
    kwargs_params = {
        "isInvisible": False,
        "userAgent": "Some specific user agent",
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }

    def test_methods_exists(self):
        assert "captcha_handler" in HCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in HCaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", HCaptchaEnm.list_values())
    def test_args(self, method: str):
        instance = HCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.pageurl
        assert instance.create_task_payload["task"]["websiteKey"] == self.sitekey

    def test_kwargs(self):
        instance = HCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            method=HCaptchaEnm.HCaptchaTaskProxyless,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    """
    Success tests
    """

    def test_basic_data(self):
        instance = HCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            method=HCaptchaEnm.HCaptchaTaskProxyless.value,
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
        instance = HCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            method=HCaptchaEnm.HCaptchaTaskProxyless.value,
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
        with HCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            method=HCaptchaEnm.HCaptchaTaskProxyless.value,
        ) as instance:
            assert instance.captcha_handler()

    async def test_context_aio_basic_data(self):
        async with HCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.sitekey,
            method=HCaptchaEnm.HCaptchaTaskProxyless.value,
        ) as instance:
            assert await instance.aio_captcha_handler()

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            HCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                websiteKey=self.sitekey,
                method=self.get_random_string(length=5),
            )
