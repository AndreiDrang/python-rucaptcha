import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import TextCaptchaEnm
from python_rucaptcha.text_captcha import TextCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestTextCaptcha(BaseTest):
    questions = (("en", "Our planet name?"), ("rn", "Название нашей планеты?"))

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in TextCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in TextCaptcha.__dict__.keys()

    def test_args(self):
        instance = TextCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == TextCaptchaEnm.TextCaptchaTask

    @pytest.mark.parametrize("lang_code, question", questions)
    def test_basic(self, lang_code: str, question: str):
        instance = TextCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, languagePool=lang_code)

        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(textcaptcha=question)

        assert isinstance(result, dict) is True

        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.parametrize("lang_code, question", questions)
    async def test_aio_basic(self, lang_code, question):
        instance = TextCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, languagePool=lang_code)

        result = await instance.aio_captcha_handler(textcaptcha=question)

        assert isinstance(result, dict) is True

        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    """
    Fail tests
    """

    def test_no_textcaptcha(self):
        with pytest.raises(TypeError):
            TextCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY).captcha_handler()
