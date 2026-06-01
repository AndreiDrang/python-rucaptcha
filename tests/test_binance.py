import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import BinanceCaptchaEnm
from python_rucaptcha.binance_captcha import BinanceCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestBinanceCaptcha(BaseTest):
    websiteURL = "https://example.com/page-with-binance"
    websiteKey = "login"
    validateId = "cb0bfefa598c4d2a8b65f31fde54ecd57b"
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
        assert "captcha_handler" in BinanceCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in BinanceCaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", BinanceCaptchaEnm.list_values())
    def test_args(self, method: str):
        kwargs = {}
        if method == BinanceCaptchaEnm.BinanceTask.value:
            kwargs = {"proxyType": "http", "proxyAddress": "1.2.3.4", "proxyPort": 8080}
        instance = BinanceCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            validateId=self.validateId,
            userAgent=self.userAgent,
            method=method,
            **kwargs,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.websiteURL
        assert instance.create_task_payload["task"]["websiteKey"] == self.websiteKey
        assert instance.create_task_payload["task"]["validateId"] == self.validateId
        assert instance.create_task_payload["task"]["userAgent"] == self.userAgent

    def test_kwargs(self):
        instance = BinanceCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            validateId=self.validateId,
            method=BinanceCaptchaEnm.BinanceTask,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    def test_proxy_params_in_payload(self):
        instance = BinanceCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            validateId=self.validateId,
            method=BinanceCaptchaEnm.BinanceTask,
            proxyType="http",
            proxyAddress="1.2.3.4",
            proxyPort=8080,
        )
        assert instance.create_task_payload["task"]["proxyType"] == "http"
        assert instance.create_task_payload["task"]["proxyAddress"] == "1.2.3.4"
        assert instance.create_task_payload["task"]["proxyPort"] == 8080

    def test_no_useragent(self):
        instance = BinanceCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            validateId=self.validateId,
            method=BinanceCaptchaEnm.BinanceTaskProxyless,
        )
        assert "userAgent" not in instance.create_task_payload["task"]

    def test_missing_proxy_for_proxy_method(self):
        with pytest.raises(ValueError, match="proxyType|proxyAddress|proxyPort"):
            BinanceCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                websiteKey=self.websiteKey,
                validateId=self.validateId,
                method=BinanceCaptchaEnm.BinanceTask,
            )

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            BinanceCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                websiteKey=self.websiteKey,
                validateId=self.validateId,
                method=self.get_random_string(5),
            )

    """
    Success tests
    """

    def test_basic_data(self):
        instance = BinanceCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            validateId=self.validateId,
            method=BinanceCaptchaEnm.BinanceTaskProxyless.value,
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
        instance = BinanceCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            validateId=self.validateId,
            method=BinanceCaptchaEnm.BinanceTaskProxyless.value,
        )

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] in ("ready", "processing")
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] in ("ERROR_CAPTCHA_UNSOLVABLE", BinanceCaptcha.NO_CAPTCHA_ERR)

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with BinanceCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            validateId=self.validateId,
            method=BinanceCaptchaEnm.BinanceTaskProxyless.value,
        ) as instance:
            assert instance

    async def test_context_aio_basic_data(self):
        async with BinanceCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            validateId=self.validateId,
            method=BinanceCaptchaEnm.BinanceTaskProxyless.value,
        ) as instance:
            assert instance

    """
    Fail tests
    """

    def test_no_websiteURL(self):
        with pytest.raises(TypeError):
            BinanceCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteKey=self.websiteKey,
                validateId=self.validateId,
            )

    def test_no_websiteKey(self):
        with pytest.raises(TypeError):
            BinanceCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                validateId=self.validateId,
            )

    def test_no_validateId(self):
        with pytest.raises(TypeError):
            BinanceCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                websiteKey=self.websiteKey,
            )
