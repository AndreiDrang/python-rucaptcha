import pytest

from src.tests.conftest import BaseTest
from python_rucaptcha.core.enums import KeyCaptchaEnm
from python_rucaptcha.key_captcha import KeyCaptcha
from python_rucaptcha.core.serializer import ResponseSer


class TestKeyCaptcha(BaseTest):
    s_s_c_user_id = "184015"
    s_s_c_session_id = "0917788cad24ad3a69813c4fcd556061"
    s_s_c_web_server_sign = "02f7f9669f1269595c4c69bcd4a3c52e"
    s_s_c_web_server_sign2 = "d888700f6f324ec0f32b44c32c50bde1"
    pageurl = "https://rucaptcha.com/demo/keycaptcha"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in KeyCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in KeyCaptcha.__dict__.keys()

    def test_basic_data(self):
        instance = KeyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            s_s_c_user_id=self.s_s_c_user_id,
            s_s_c_session_id=self.s_s_c_session_id,
            s_s_c_web_server_sign=self.s_s_c_web_server_sign,
            s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
            method=KeyCaptchaEnm.KEYCAPTCHA.value,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == KeyCaptchaEnm.KEYCAPTCHA.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["s_s_c_user_id"] == self.s_s_c_user_id
        assert instance.post_payload["s_s_c_session_id"] == self.s_s_c_session_id
        assert instance.post_payload["s_s_c_web_server_sign"] == self.s_s_c_web_server_sign
        assert instance.post_payload["s_s_c_web_server_sign2"] == self.s_s_c_web_server_sign2

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = KeyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            s_s_c_user_id=self.s_s_c_user_id,
            s_s_c_session_id=self.s_s_c_session_id,
            s_s_c_web_server_sign=self.s_s_c_web_server_sign,
            s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
            method=KeyCaptchaEnm.KEYCAPTCHA.value,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == KeyCaptchaEnm.KEYCAPTCHA.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["s_s_c_user_id"] == self.s_s_c_user_id
        assert instance.post_payload["s_s_c_session_id"] == self.s_s_c_session_id
        assert instance.post_payload["s_s_c_web_server_sign"] == self.s_s_c_web_server_sign
        assert instance.post_payload["s_s_c_web_server_sign2"] == self.s_s_c_web_server_sign2

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == ResponseSer().dict().keys()

    def test_context_basic_data(self):
        with KeyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            s_s_c_user_id=self.s_s_c_user_id,
            s_s_c_session_id=self.s_s_c_session_id,
            s_s_c_web_server_sign=self.s_s_c_web_server_sign,
            s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
            method=KeyCaptchaEnm.KEYCAPTCHA.value,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == KeyCaptchaEnm.KEYCAPTCHA.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["s_s_c_user_id"] == self.s_s_c_user_id
            assert instance.post_payload["s_s_c_session_id"] == self.s_s_c_session_id
            assert instance.post_payload["s_s_c_web_server_sign"] == self.s_s_c_web_server_sign
            assert instance.post_payload["s_s_c_web_server_sign2"] == self.s_s_c_web_server_sign2

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with KeyCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            s_s_c_user_id=self.s_s_c_user_id,
            s_s_c_session_id=self.s_s_c_session_id,
            s_s_c_web_server_sign=self.s_s_c_web_server_sign,
            s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
            method=KeyCaptchaEnm.KEYCAPTCHA.value,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == KeyCaptchaEnm.KEYCAPTCHA.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["s_s_c_user_id"] == self.s_s_c_user_id
            assert instance.post_payload["s_s_c_session_id"] == self.s_s_c_session_id
            assert instance.post_payload["s_s_c_web_server_sign"] == self.s_s_c_web_server_sign
            assert instance.post_payload["s_s_c_web_server_sign2"] == self.s_s_c_web_server_sign2

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            KeyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                s_s_c_user_id=self.s_s_c_user_id,
                s_s_c_session_id=self.s_s_c_session_id,
                s_s_c_web_server_sign=self.s_s_c_web_server_sign,
                s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
                method=self.get_random_string(length=5),
            )

    def test_no_pageurl(self):
        with pytest.raises(TypeError):
            KeyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                s_s_c_user_id=self.s_s_c_user_id,
                s_s_c_session_id=self.s_s_c_session_id,
                s_s_c_web_server_sign=self.s_s_c_web_server_sign,
                s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
                method=KeyCaptchaEnm.KEYCAPTCHA.value,
            )

    def test_no_s_s_c_user_id(self):
        with pytest.raises(TypeError):
            KeyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                s_s_c_session_id=self.s_s_c_session_id,
                s_s_c_web_server_sign=self.s_s_c_web_server_sign,
                s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
                method=KeyCaptchaEnm.KEYCAPTCHA.value,
            )

    def test_no_s_s_c_web_server_sign(self):
        with pytest.raises(TypeError):
            KeyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                s_s_c_user_id=self.s_s_c_user_id,
                s_s_c_session_id=self.s_s_c_session_id,
                s_s_c_web_server_sign2=self.s_s_c_web_server_sign2,
                method=KeyCaptchaEnm.KEYCAPTCHA.value,
            )

    def test_no_s_s_c_web_server_sign2(self):
        with pytest.raises(TypeError):
            KeyCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                s_s_c_user_id=self.s_s_c_user_id,
                s_s_c_session_id=self.s_s_c_session_id,
                s_s_c_web_server_sign=self.s_s_c_web_server_sign,
                method=KeyCaptchaEnm.KEYCAPTCHA.value,
            )
