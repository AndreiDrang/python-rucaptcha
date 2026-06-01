import pytest

from tests.conftest import BaseTest
from python_rucaptcha.vk_captcha import VKCaptcha
from python_rucaptcha.core.enums import VKCaptchaEnm
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestVKCaptcha(BaseTest):
    redirectUri = "https://id.vk.com/not_robot_captcha?domain=vk.com"
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    captcha_link = "https://vk.com/captcha.php?sid=123456"

    def test_methods_exists(self):
        assert "captcha_handler" in VKCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in VKCaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", VKCaptchaEnm.list_values())
    def test_args(self, method: str):
        instance = VKCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            method=method,
            redirectUri=self.redirectUri,
            userAgent=self.userAgent,
            proxyType="socks5",
            proxyAddress=self.proxyAddress,
            proxyPort=self.proxyPort,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method

    def test_vkcaptcha_task_payload(self):
        instance = VKCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            redirectUri=self.redirectUri,
            userAgent=self.userAgent,
            proxyType="socks5",
            proxyAddress=self.proxyAddress,
            proxyPort=self.proxyPort,
        )
        task = instance.create_task_payload["task"]
        assert task["type"] == "VKCaptchaTask"
        assert task["redirectUri"] == self.redirectUri
        assert task["userAgent"] == self.userAgent
        assert task["proxyType"] == "socks5"
        assert task["proxyAddress"] == self.proxyAddress
        assert task["proxyPort"] == self.proxyPort

    def test_vkcaptcha_task_with_proxy_auth(self):
        instance = VKCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            redirectUri=self.redirectUri,
            userAgent=self.userAgent,
            proxyType="socks5",
            proxyAddress=self.proxyAddress,
            proxyPort=self.proxyPort,
            proxyLogin="user1",
            proxyPassword="pass1",
        )
        task = instance.create_task_payload["task"]
        assert task["proxyLogin"] == "user1"
        assert task["proxyPassword"] == "pass1"

    def test_vkcaptcha_image_task_no_proxy_required(self):
        instance = VKCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            method=VKCaptchaEnm.VKCaptchaImageTask,
        )
        assert instance.create_task_payload["task"]["type"] == "VKCaptchaImageTask"
        assert "redirectUri" not in instance.create_task_payload["task"]

    def test_vkcaptcha_image_task_default_method(self):
        instance = VKCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
        )
        assert instance.create_task_payload["task"]["type"] == "VKCaptchaTask"

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            VKCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                method=self.get_random_string(length=5),
            )

    def test_vkcaptcha_task_missing_required_params(self):
        with pytest.raises(ValueError):
            VKCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                method=VKCaptchaEnm.VKCaptchaTask,
            )

    def test_vkcaptcha_task_missing_proxy(self):
        with pytest.raises(ValueError):
            VKCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                redirectUri=self.redirectUri,
                userAgent=self.userAgent,
                method=VKCaptchaEnm.VKCaptchaTask,
            )

    """
    Success tests
    """

    def test_basic_data(self):
        instance = VKCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            redirectUri=self.redirectUri,
            userAgent=self.userAgent,
            proxyType="socks5",
            proxyAddress=self.proxyAddress,
            proxyPort=self.proxyPort,
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
        instance = VKCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            redirectUri=self.redirectUri,
            userAgent=self.userAgent,
            proxyType="socks5",
            proxyAddress=self.proxyAddress,
            proxyPort=self.proxyPort,
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
        with VKCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            redirectUri=self.redirectUri,
            userAgent=self.userAgent,
            proxyType="socks5",
            proxyAddress=self.proxyAddress,
            proxyPort=self.proxyPort,
        ) as instance:
            assert instance

    async def test_context_aio_basic_data(self):
        async with VKCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            redirectUri=self.redirectUri,
            userAgent=self.userAgent,
            proxyType="socks5",
            proxyAddress=self.proxyAddress,
            proxyPort=self.proxyPort,
        ) as instance:
            assert instance
