import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import ReCaptchaEnm
from python_rucaptcha.re_captcha import ReCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestReCaptcha(BaseTest):
    googlekey = "6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH"
    pageurl = "https://rucaptcha.com/demo/recaptcha-v2"
    kwargs_params = {
        "recaptchaDataSValue": "sample-recaptchaDataSValue",
        "isInvisible": True,
        "userAgent": "Some specific user agent",
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }

    @pytest.mark.parametrize("method", ReCaptchaEnm.list_values())
    def test_args(self, method: str):
        instance = ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.pageurl
        assert instance.create_task_payload["task"]["websiteKey"] == self.googlekey

    def test_kwargs(self):
        instance = ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in ReCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in ReCaptcha.__dict__.keys()

    def test_basic_data(self):
        instance = ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
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
        instance = ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
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
        with ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
        ) as instance:
            assert instance.captcha_handler()

    async def test_context_aio_basic_data(self):
        async with ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
        ) as instance:
            assert await instance.aio_captcha_handler()

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            ReCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
                method=self.get_random_string(length=5),
            )
