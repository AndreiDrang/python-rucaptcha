import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import KeyCaptchaEnm
from python_rucaptcha.key_captcha import KeyCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestKeyCaptcha(BaseTest):
    s_s_c_user_id = "184015"
    s_s_c_session_id = "0917788cad24ad3a69813c4fcd556061"
    s_s_c_web_server_sign = "02f7f9669f1269595c4c69bcd4a3c52e"
    s_s_c_web_server_sign2 = "d888700f6f324ec0f32b44c32c50bde1"
    pageurl = "https://rucaptcha.com/demo/keycaptcha"
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
        assert "captcha_handler" in KeyCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in KeyCaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", KeyCaptchaEnm.list_values())
    def test_args(self, method: str):
        instance = KeyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            s_s_c_user_id=self.s_s_c_user_id,
            s_s_c_session_id=self.s_s_c_session_id,
            s_s_c_web_server_sign=self.s_s_c_web_server_sign,
            s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.pageurl
        assert instance.create_task_payload["task"]["s_s_c_user_id"] == self.s_s_c_user_id
        assert instance.create_task_payload["task"]["s_s_c_session_id"] == self.s_s_c_session_id
        assert instance.create_task_payload["task"]["s_s_c_web_server_sign"] == self.s_s_c_web_server_sign
        assert instance.create_task_payload["task"]["s_s_c_web_server_sign2"] == self.s_s_c_web_server_sign2

    def test_kwargs(self):
        instance = KeyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            s_s_c_user_id=self.s_s_c_user_id,
            s_s_c_session_id=self.s_s_c_session_id,
            s_s_c_web_server_sign=self.s_s_c_web_server_sign,
            s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
            method=KeyCaptchaEnm.KeyCaptchaTaskProxyless,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    def test_basic_data(self):
        instance = KeyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            s_s_c_user_id=self.s_s_c_user_id,
            s_s_c_session_id=self.s_s_c_session_id,
            s_s_c_web_server_sign=self.s_s_c_web_server_sign,
            s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
            method=KeyCaptchaEnm.KeyCaptchaTaskProxyless.value,
        )

        result = instance.captcha_handler()

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    async def test_aio_basic_data(self):
        instance = KeyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            s_s_c_user_id=self.s_s_c_user_id,
            s_s_c_session_id=self.s_s_c_session_id,
            s_s_c_web_server_sign=self.s_s_c_web_server_sign,
            s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
            method=KeyCaptchaEnm.KeyCaptchaTaskProxyless.value,
        )

        result = instance.captcha_handler()

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with KeyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            s_s_c_user_id=self.s_s_c_user_id,
            s_s_c_session_id=self.s_s_c_session_id,
            s_s_c_web_server_sign=self.s_s_c_web_server_sign,
            s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
            method=KeyCaptchaEnm.KeyCaptchaTaskProxyless.value,
        ) as instance:
            assert instance

    async def test_context_aio_basic_data(self):
        async with KeyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            s_s_c_user_id=self.s_s_c_user_id,
            s_s_c_session_id=self.s_s_c_session_id,
            s_s_c_web_server_sign=self.s_s_c_web_server_sign,
            s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
            method=KeyCaptchaEnm.KeyCaptchaTaskProxyless.value,
        ) as instance:
            assert instance

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            KeyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                s_s_c_user_id=self.s_s_c_user_id,
                s_s_c_session_id=self.s_s_c_session_id,
                s_s_c_web_server_sign=self.s_s_c_web_server_sign,
                s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
                method=self.get_random_string(length=5),
            )

    @pytest.mark.parametrize("method", KeyCaptchaEnm.list_values())
    def test_no_websiteURL(self, method):
        with pytest.raises(TypeError):
            KeyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                s_s_c_user_id=self.s_s_c_user_id,
                s_s_c_session_id=self.s_s_c_session_id,
                s_s_c_web_server_sign=self.s_s_c_web_server_sign,
                s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
                method=method,
            )

    @pytest.mark.parametrize("method", KeyCaptchaEnm.list_values())
    def test_no_s_s_c_user_id(self, method: str):
        with pytest.raises(TypeError):
            KeyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                s_s_c_session_id=self.s_s_c_session_id,
                s_s_c_web_server_sign=self.s_s_c_web_server_sign,
                s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
                method=method,
            )

    @pytest.mark.parametrize("method", KeyCaptchaEnm.list_values())
    def test_no_s_s_c_web_server_sign(self, method: str):
        with pytest.raises(TypeError):
            KeyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                s_s_c_user_id=self.s_s_c_user_id,
                s_s_c_session_id=self.s_s_c_session_id,
                s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
                method=method,
            )

    @pytest.mark.parametrize("method", KeyCaptchaEnm.list_values())
    def test_no_s_s_c_web_server_sign2(self, method: str):
        with pytest.raises(TypeError):
            KeyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                s_s_c_user_id=self.s_s_c_user_id,
                s_s_c_session_id=self.s_s_c_session_id,
                s_s_c_web_server_sign=self.s_s_c_web_server_sign,
                method=method,
            )
