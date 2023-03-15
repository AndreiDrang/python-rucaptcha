import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import YandexSmartCaptchaEnm
from python_rucaptcha.core.serializer import ResponseSer
from python_rucaptcha.yandex_smart_captcha import YandexSmartCaptcha


class TestYandexSmartCaptcha(BaseTest):
    pageurl = "https://captcha-api.yandex.ru/demo"
    sitekey = "FEXfAbHQsToo97VidNVk3j4dC74nGW1DgdxjtNB9"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in YandexSmartCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in YandexSmartCaptcha.__dict__.keys()

    def test_basic_data(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            sitekey=self.sitekey,
            method=YandexSmartCaptchaEnm.YANDEX.value,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == YandexSmartCaptchaEnm.YANDEX.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["sitekey"] == self.sitekey

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            sitekey=self.sitekey,
            method=YandexSmartCaptchaEnm.YANDEX.value,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == YandexSmartCaptchaEnm.YANDEX.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["sitekey"] == self.sitekey

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == ResponseSer().dict().keys()

    def test_context_basic_data(self):
        with YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            sitekey=self.sitekey,
            method=YandexSmartCaptchaEnm.YANDEX.value,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == YandexSmartCaptchaEnm.YANDEX.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["sitekey"] == self.sitekey

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            sitekey=self.sitekey,
            method=YandexSmartCaptchaEnm.YANDEX.value,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == YandexSmartCaptchaEnm.YANDEX.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["sitekey"] == self.sitekey

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            YandexSmartCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                sitekey=self.sitekey,
                method=self.get_random_string(5),
            )
