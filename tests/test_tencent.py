import pytest

from tests.conftest import BaseTest
from python_rucaptcha.tencent import Tencent
from python_rucaptcha.core.enums import TencentEnm


class TestTencent(BaseTest):
    websiteURL = "https://www.tencentcloud.com/account/register"
    appId = "2009899766"

    kwargs_params = {
        "proxyLogin": "user23",
        "proxyPassword": "p4$$w0rd",
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }

    def test_methods_exists(self):
        assert "captcha_handler" in Tencent.__dict__.keys()
        assert "aio_captcha_handler" in Tencent.__dict__.keys()

    @pytest.mark.parametrize("method", TencentEnm.list_values())
    def test_args(self, method: str):
        instance = Tencent(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            appId=self.appId,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.websiteURL
        assert instance.create_task_payload["task"]["appId"] == self.appId

    @pytest.mark.parametrize("method", TencentEnm.list_values())
    def test_kwargs(self, method: str):
        instance = Tencent(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            appId=self.appId,
            method=method,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    """
    Fail tests
    """

    @pytest.mark.parametrize("method", TencentEnm.list_values())
    def test_no_websiteURL(self, method: str):
        with pytest.raises(TypeError):
            Tencent(rucaptcha_key=self.RUCAPTCHA_KEY, appId=self.appId, method=method)

    @pytest.mark.parametrize("method", TencentEnm.list_values())
    def test_no_appId(self, method: str):
        with pytest.raises(TypeError):
            Tencent(rucaptcha_key=self.RUCAPTCHA_KEY, websiteURL=self.websiteURL, method=method)

    @pytest.mark.parametrize("method", TencentEnm.list_values())
    def test_wrong_method(self, method: str):
        with pytest.raises(ValueError):
            Tencent(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                appId=self.appId,
                method=self.get_random_string(length=5),
            )
