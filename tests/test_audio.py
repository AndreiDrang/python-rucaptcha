import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import SaveFormatsEnm
from python_rucaptcha.audio_captcha import AudioCaptcha
from python_rucaptcha.core.serializer import ResponseSer


class TestAudioCaptcha(BaseTest):
    captcha_file = "src/examples/mediacaptcha_audio/recaptcha_55914.mp3"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in AudioCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in AudioCaptcha.__dict__.keys()

    def test_basic_data_file(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(captcha_file=self.captcha_file)

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

    def test_basic_data_file_const(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=SaveFormatsEnm.CONST)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(captcha_file=self.captcha_file)

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
    async def test_aio_basic_data_file(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler(captcha_file=self.captcha_file)

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
    async def test_aio_basic_data_file_const(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=SaveFormatsEnm.CONST)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler(captcha_file=self.captcha_file)

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

    """
    Fail tests
    """

    def test_no_captcha(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == AudioCaptcha.NO_CAPTCHA_ERR
        assert result["captchaSolve"] == {}

        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_no_captcha(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == AudioCaptcha.NO_CAPTCHA_ERR
        assert result["captchaSolve"] == {}
        assert result.keys() == ResponseSer().dict().keys()

    """
    Failed tests
    """

    def test_wrong_link(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(captcha_link=self.get_random_string(length=50))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == ResponseSer().dict().keys()

    def test_wrong_path(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        with pytest.raises(FileNotFoundError):
            result = instance.captcha_handler(captcha_file=self.get_random_string(length=50))

            assert isinstance(result, dict) is True
            assert result["error"] is True
            assert result["taskId"] is None
            assert result["captchaSolve"] == {}
            assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_link(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler(captcha_link=self.get_random_string(length=50))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_path(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        with pytest.raises(FileNotFoundError):
            result = await instance.aio_captcha_handler(captcha_file=self.get_random_string(length=50))

            assert isinstance(result, dict) is True
            assert result["error"] is True
            assert result["taskId"] is None
            assert result["captchaSolve"] == {}
            assert result.keys() == ResponseSer().dict().keys()
