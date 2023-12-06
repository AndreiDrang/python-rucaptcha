import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import SaveFormatsEnm
from python_rucaptcha.audio_captcha import AudioCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestAudioCaptcha(BaseTest):
    captcha_file = "src/examples/mediacaptcha_audio/recaptcha_55914.mp3"
    captcha_link = "https://github.com/AndreiDrang/python-rucaptcha/raw/3631e399f9cfa2e81c3f2920f9d79fdc2fd91f85/src/examples/mediacaptcha_audio/recaptcha_55914.mp3"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in AudioCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in AudioCaptcha.__dict__.keys()

    def test_args(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY

    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    def test_basic_data_file(self, save_format):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        result = instance.captcha_handler(captcha_file=self.captcha_file)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["token"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    def test_basic_data_link(self, save_format):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        result = instance.captcha_handler(captcha_link=self.captcha_link)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["token"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    def test_basic_data_base64(self, save_format):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        with open(self.captcha_file, "rb") as f:
            result = instance.captcha_handler(captcha_base64=f.read())

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["token"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    async def test_aio_basic_data_file(self, save_format):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        result = await instance.aio_captcha_handler(captcha_file=self.captcha_file)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["token"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    async def test_aio_basic_data_link(self, save_format):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        result = await instance.aio_captcha_handler(captcha_link=self.captcha_link)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["token"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    async def test_aio_basic_data_base64(self, save_format):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        with open(self.captcha_file, "rb") as f:
            result = await instance.aio_captcha_handler(captcha_base64=f.read())

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["token"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    """
    Fail tests
    """

    def test_no_captcha(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["solution"]["token"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_no_captcha(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["solution"]["token"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_wrong_link(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = instance.captcha_handler(captcha_link=self.get_random_string(length=50))

        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["solution"]["token"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_wrong_path(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        with pytest.raises(FileNotFoundError):
            instance.captcha_handler(captcha_file=self.get_random_string(length=50))

    def test_wrong_base64(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = instance.captcha_handler(captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8"))

        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["solution"]["token"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_link(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = await instance.aio_captcha_handler(captcha_link=self.get_random_string(length=50))

        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["solution"]["token"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_path(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        with pytest.raises(FileNotFoundError):
            await instance.aio_captcha_handler(captcha_file=self.get_random_string(length=50))

    @pytest.mark.asyncio
    async def test_aio_wrong_base64(self):
        instance = AudioCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = await instance.aio_captcha_handler(
            captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8")
        )

        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["solution"]["token"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()
