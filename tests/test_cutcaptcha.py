import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import CutCaptchaEnm
from python_rucaptcha.cutcaptcha import CutCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestCutCaptcha(BaseTest):
    miseryKey = "a1488b66da00bf332a1488993a5443c79047e752"
    pageurl = "https://example.cc/foo/bar.html"
    apiKey = "SAb83IIB"

    kwargs_params = {
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }

    def test_methods_exists(self):
        assert "captcha_handler" in CutCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in CutCaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", CutCaptchaEnm.list_values())
    def test_args(self, method: str):
        instance = CutCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            miseryKey=self.miseryKey,
            apiKey=self.apiKey,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.pageurl
        assert instance.create_task_payload["task"]["miseryKey"] == self.miseryKey
        assert instance.create_task_payload["task"]["apiKey"] == self.apiKey

    def test_kwargs(self):
        instance = CutCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            miseryKey=self.miseryKey,
            apiKey=self.apiKey,
            method=CutCaptchaEnm.CutCaptchaTaskProxyless,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    """
    Success tests
    """

    def test_basic_data(self):
        instance = CutCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            miseryKey=self.miseryKey,
            apiKey=self.apiKey,
            method=CutCaptchaEnm.CutCaptchaTaskProxyless.value,
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
        instance = CutCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            miseryKey=self.miseryKey,
            apiKey=self.apiKey,
            method=CutCaptchaEnm.CutCaptchaTaskProxyless.value,
        )

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"], dict) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] in ("ERROR_CAPTCHA_UNSOLVABLE", CutCaptcha.NO_CAPTCHA_ERR)

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with CutCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            miseryKey=self.miseryKey,
            apiKey=self.apiKey,
            method=CutCaptchaEnm.CutCaptchaTaskProxyless.value,
        ) as instance:
            assert instance.captcha_handler()

    async def test_context_aio_basic_data(self):
        async with CutCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            miseryKey=self.miseryKey,
            apiKey=self.apiKey,
            method=CutCaptchaEnm.CutCaptchaTaskProxyless.value,
        ) as instance:
            assert await instance.aio_captcha_handler()

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            CutCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                miseryKey=self.miseryKey,
                apiKey=self.apiKey,
                method=self.get_random_string(length=5),
            )

    def test_no_websiteURL(self):
        with pytest.raises(TypeError):
            CutCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                miseryKey=self.miseryKey,
                apiKey=self.apiKey,
                method=self.get_random_string(length=5),
            )

    def test_no_miseryKey(self):
        with pytest.raises(TypeError):
            CutCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                apiKey=self.apiKey,
                method=self.get_random_string(length=5),
            )

    def test_no_apiKey(self):
        with pytest.raises(TypeError):
            CutCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                miseryKey=self.miseryKey,
                method=self.get_random_string(length=5),
            )
