import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import FunCaptchaEnm
from python_rucaptcha.fun_captcha import FunCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestFunCaptcha(BaseTest):
    publickey = "69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC"
    pageurl = (
        "https://api.funcaptcha.com/tile-game-lite-mode/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC&lang=en"
    )
    surl = "https://client-api.arkoselabs.com"
    kwargs_params = {
        "funcaptchaApiJSSubdomain": "sample-api.arkoselabs.com",
        "userAgent": "Some specific user agent",
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }
    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in FunCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in FunCaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", FunCaptchaEnm.list_values())
    def test_args(self, method: str):
        instance = FunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websitePublicKey=self.publickey,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.pageurl

    def test_kwargs(self):
        instance = FunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websitePublicKey=self.publickey,
            method=FunCaptchaEnm.FunCaptchaTaskProxyless,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    def test_basic_data(self):
        instance = FunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websitePublicKey=self.publickey,
            method=FunCaptchaEnm.FunCaptchaTaskProxyless.value,
        )

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = FunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websitePublicKey=self.publickey,
            method=FunCaptchaEnm.FunCaptchaTaskProxyless.value,
        )

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with FunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websitePublicKey=self.publickey,
            method=FunCaptchaEnm.FunCaptchaTaskProxyless.value,
        ) as instance:
            assert instance.captcha_handler()

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with FunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            websitePublicKey=self.publickey,
            method=FunCaptchaEnm.FunCaptchaTaskProxyless.value,
        ) as instance:
            assert await instance.aio_captcha_handler()

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            FunCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                websitePublicKey=self.publickey,
                method=self.get_random_string(length=5),
            )
