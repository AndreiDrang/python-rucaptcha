import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import YidunEnm
from python_rucaptcha.yidun_captcha import YidunCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestYidunCaptcha(BaseTest):
    websiteURL = "https://example.com/page-with-yidun"
    websiteKey = "0f743r3g1grz3grz0ym5"
    userAgent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    )
    kwargs_params = {
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }

    def test_methods_exists(self):
        assert "captcha_handler" in YidunCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in YidunCaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", YidunEnm.list_values())
    def test_args(self, method: str):
        kwargs = {}
        if method == YidunEnm.YidunTask.value:
            kwargs = {"proxyType": "http", "proxyAddress": "1.2.3.4", "proxyPort": 8080}
        instance = YidunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            userAgent=self.userAgent,
            method=method,
            **kwargs,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.websiteURL
        assert instance.create_task_payload["task"]["websiteKey"] == self.websiteKey
        assert instance.create_task_payload["task"]["userAgent"] == self.userAgent

    def test_kwargs(self):
        instance = YidunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YidunEnm.YidunTask,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    def test_enterprise_params(self):
        enterprise_params = {
            "yidunGetLib": "https://example.com/yidun/load.min.js",
            "yidunApiServerSubdomain": "c.dun.163.com",
            "challenge": "0c59ba0d1b2349f9b2c1a2b3c4d5e6f7",
            "hcg": "2c78a7731e2345f6a7b8c9d0e1f2a3b4",
            "hct": 1779358333191,
        }
        instance = YidunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            **enterprise_params,
        )
        for key, value in enterprise_params.items():
            assert instance.create_task_payload["task"][key] == value

    def test_no_useragent(self):
        instance = YidunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YidunEnm.YidunTaskProxyless,
        )
        assert "userAgent" not in instance.create_task_payload["task"]

    def test_proxy_params_in_payload(self):
        instance = YidunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YidunEnm.YidunTask,
            proxyType="http",
            proxyAddress="1.2.3.4",
            proxyPort=8080,
        )
        assert instance.create_task_payload["task"]["proxyType"] == "http"
        assert instance.create_task_payload["task"]["proxyAddress"] == "1.2.3.4"
        assert instance.create_task_payload["task"]["proxyPort"] == 8080

    def test_missing_proxy_for_proxy_method(self):
        with pytest.raises(ValueError, match="proxyType|proxyAddress|proxyPort"):
            YidunCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                websiteKey=self.websiteKey,
                method=YidunEnm.YidunTask,
            )

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            YidunCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                websiteKey=self.websiteKey,
                method=self.get_random_string(5),
            )

    """
    Success tests
    """

    def test_basic_data(self):
        instance = YidunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YidunEnm.YidunTaskProxyless.value,
        )

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] in ("ready", "processing")
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    async def test_aio_basic_data(self):
        instance = YidunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YidunEnm.YidunTaskProxyless.value,
        )

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] in ("ready", "processing")
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] in ("ERROR_CAPTCHA_UNSOLVABLE", YidunCaptcha.NO_CAPTCHA_ERR)

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with YidunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YidunEnm.YidunTaskProxyless.value,
        ) as instance:
            assert instance

    async def test_context_aio_basic_data(self):
        async with YidunCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YidunEnm.YidunTaskProxyless.value,
        ) as instance:
            assert instance

    """
    Fail tests
    """

    def test_no_websiteURL(self):
        with pytest.raises(TypeError):
            YidunCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteKey=self.websiteKey,
            )

    def test_no_websiteKey(self):
        with pytest.raises(TypeError):
            YidunCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
            )
