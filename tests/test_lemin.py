import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import LeminCaptchaEnm
from python_rucaptcha.lemin_captcha import LeminCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestLeminCroppedCaptcha(BaseTest):
    pageurl = "https://dashboard.leminnow.com/auth/signup"
    api_server = "api.leminnow.com"
    div_id = "lemin-cropped-captcha"
    captcha_id = "CROPPED_099216d_8ba061383fa24ef498115023aa7189d4"
    kwargs_params = {
        "leminApiServerSubdomain": "https://api.leminnow.com/",
        "userAgent": "Some specific user agent",
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }

    def test_methods_exists(self):
        assert "captcha_handler" in LeminCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in LeminCaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", LeminCaptchaEnm.list_values())
    def test_args(self, method: str):
        instance = LeminCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            captchaId=self.captcha_id,
            div_id=self.div_id,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.pageurl

    def test_kwargs(self):
        instance = LeminCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            captchaId=self.captcha_id,
            div_id=self.div_id,
            method=LeminCaptchaEnm.LeminTaskProxyless,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    """
    Success tests
    """

    def test_basic_data(self):
        instance = LeminCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            captchaId=self.captcha_id,
            div_id=self.div_id,
            api_server=self.api_server,
            method=LeminCaptchaEnm.LeminTaskProxyless.value,
        )

        result = instance.captcha_handler()

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    async def test_aio_basic_data(self):
        instance = LeminCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            captchaId=self.captcha_id,
            div_id=self.div_id,
            api_server=self.api_server,
            method=LeminCaptchaEnm.LeminTaskProxyless.value,
        )

        result = await instance.aio_captcha_handler()

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with LeminCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            captchaId=self.captcha_id,
            div_id=self.div_id,
            method=LeminCaptchaEnm.LeminTaskProxyless.value,
        ) as instance:
            assert instance.captcha_handler()

    async def test_context_aio_basic_data(self):
        async with LeminCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            captchaId=self.captcha_id,
            div_id=self.div_id,
            method=LeminCaptchaEnm.LeminTaskProxyless.value,
        ) as instance:
            assert await instance.aio_captcha_handler()

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            LeminCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                captchaId=self.captcha_id,
                div_id=self.div_id,
                api_server=self.api_server,
                method=self.get_random_string(length=5),
            )

    def test_no_websiteURL(self):
        with pytest.raises(TypeError):
            LeminCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                captchaId=self.captcha_id,
                div_id=self.div_id,
                method=self.get_random_string(length=5),
            )

    def test_no_div_id(self):
        with pytest.raises(TypeError):
            LeminCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                captchaId=self.captcha_id,
                method=self.get_random_string(length=5),
            )

    def test_no_captchaId(self):
        with pytest.raises(TypeError):
            LeminCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                div_id=self.div_id,
                method=self.get_random_string(length=5),
            )
