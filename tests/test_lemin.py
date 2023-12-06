import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import LeminCroppedCaptchaEnm
from python_rucaptcha.core.serializer import GetTaskResultResponseSer
from python_rucaptcha.lemin_cropped_captcha import LeminCroppedCaptcha


class TestLeminCroppedCaptcha(BaseTest):
    pageurl = "https://dashboard.leminnow.com/auth/signup"
    api_server = "api.leminnow.com"
    div_id = "lemin-cropped-captcha"
    captcha_id = "CROPPED_099216d_8ba061383fa24ef498115023aa7189d4"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in LeminCroppedCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in LeminCroppedCaptcha.__dict__.keys()

    def test_basic_data(self):
        instance = LeminCroppedCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            captcha_id=self.captcha_id,
            div_id=self.div_id,
            api_server=self.api_server,
            method=LeminCroppedCaptchaEnm.LeminTaskProxyless.value,
        )

        assert instance.create_task_payload["method"] == LeminCroppedCaptchaEnm.LeminTaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["captcha_id"] == self.captcha_id
        assert instance.create_task_payload["div_id"] == self.div_id
        assert instance.create_task_payload["api_server"] == self.api_server

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], dict) is True
        else:
            assert result["error"] is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = LeminCroppedCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            captcha_id=self.captcha_id,
            div_id=self.div_id,
            api_server=self.api_server,
            method=LeminCroppedCaptchaEnm.LeminTaskProxyless.value,
        )

        assert instance.create_task_payload["method"] == LeminCroppedCaptchaEnm.LeminTaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["captcha_id"] == self.captcha_id
        assert instance.create_task_payload["div_id"] == self.div_id
        assert instance.create_task_payload["api_server"] == self.api_server

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], dict) is True
        else:
            assert result["error"] is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with LeminCroppedCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            captcha_id=self.captcha_id,
            div_id=self.div_id,
            method=LeminCroppedCaptchaEnm.LeminTaskProxyless.value,
        ) as instance:
            assert instance.create_task_payload["method"] == LeminCroppedCaptchaEnm.LeminTaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["captcha_id"] == self.captcha_id
            assert instance.create_task_payload["div_id"] == self.div_id

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with LeminCroppedCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            captcha_id=self.captcha_id,
            div_id=self.div_id,
            method=LeminCroppedCaptchaEnm.LeminTaskProxyless.value,
        ) as instance:
            assert instance.create_task_payload["method"] == LeminCroppedCaptchaEnm.LeminTaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["captcha_id"] == self.captcha_id
            assert instance.create_task_payload["div_id"] == self.div_id

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            LeminCroppedCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                captcha_id=self.captcha_id,
                div_id=self.div_id,
                api_server=self.api_server,
                method=self.get_random_string(length=5),
            )

    def test_no_pageurl(self):
        with pytest.raises(TypeError):
            LeminCroppedCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                captcha_id=self.captcha_id,
                div_id=self.div_id,
                method=self.get_random_string(length=5),
            )

    def test_no_div_id(self):
        with pytest.raises(TypeError):
            LeminCroppedCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                captcha_id=self.captcha_id,
                method=self.get_random_string(length=5),
            )

    def test_no_captcha_id(self):
        with pytest.raises(TypeError):
            LeminCroppedCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                div_id=self.div_id,
                method=self.get_random_string(length=5),
            )
