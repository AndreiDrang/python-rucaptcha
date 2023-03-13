import pytest

from src.tests.conftest import BaseTest
from python_rucaptcha.text_captcha import TextCaptcha
from python_rucaptcha.core.serializer import ResponseSer


class TestTextCaptcha(BaseTest):
    questions = ((0, "Our planet name?"), (1, "Название нашей планеты?"), (2, "Our planet name?"))

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in TextCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in TextCaptcha.__dict__.keys()

    @pytest.mark.parametrize("lang_code, question", questions)
    def test_basic_data(self, lang_code, question):
        instance = TextCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, language=lang_code)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(textcaptcha=question)

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert result["taskId"].isnumeric() is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("lang_code, question", questions)
    async def test_aio_basic_data(self, lang_code, question):
        instance = TextCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, language=lang_code)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler(textcaptcha=question)

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert result["taskId"].isnumeric() is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == ResponseSer().dict().keys()

    """
    Fail tests
    """

    def test_no_textcaptcha(self):
        with pytest.raises(TypeError):
            TextCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY).captcha_handler()
