import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import FriendlyCaptchaEnm
from python_rucaptcha.core.serializer import GetTaskResultResponseSer
from python_rucaptcha.friendly_captcha import FriendlyCaptcha


class TestFriendlyCaptcha(BaseTest):
    websiteURL = "https://example.cc/foo/bar.html"
    websiteKey = "SAb83IIB"

    kwargs_params = {
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }

    def test_methods_exists(self):
        assert "captcha_handler" in FriendlyCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in FriendlyCaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", FriendlyCaptchaEnm.list_values())
    def test_args(self, method: str):
        instance = FriendlyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.websiteURL
        assert instance.create_task_payload["task"]["websiteKey"] == self.websiteKey

    def test_kwargs(self):
        instance = FriendlyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=FriendlyCaptchaEnm.FriendlyCaptchaTaskProxyless,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    """
    Success tests
    """

    def test_basic_data(self):
        instance = FriendlyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=FriendlyCaptchaEnm.FriendlyCaptchaTaskProxyless.value,
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
        instance = FriendlyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=FriendlyCaptchaEnm.FriendlyCaptchaTaskProxyless.value,
        )

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] in ("ready", "processing")
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] in ("ERROR_CAPTCHA_UNSOLVABLE", FriendlyCaptcha.NO_CAPTCHA_ERR)

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with FriendlyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=FriendlyCaptchaEnm.FriendlyCaptchaTaskProxyless.value,
        ) as instance:
            assert instance

    async def test_context_aio_basic_data(self):
        async with FriendlyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=FriendlyCaptchaEnm.FriendlyCaptchaTaskProxyless.value,
        ) as instance:
            assert instance

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            FriendlyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                websiteKey=self.websiteKey,
                method=self.get_random_string(length=5),
            )

    def test_no_websiteURL(self):
        with pytest.raises(TypeError):
            FriendlyCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, websiteKey=self.websiteKey)

    def test_no_websiteKey(self):
        with pytest.raises(TypeError):
            FriendlyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
            )
