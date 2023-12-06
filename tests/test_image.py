import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import SaveFormatsEnm
from python_rucaptcha.image_captcha import ImageCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class BaseImageCaptcha(BaseTest):
    captcha_file = "src/examples/088636.jpg"
    captcha_url = "https://rucaptcha.com/dist/web/99581b9d446a509a0a01954438a5e36a.jpg"


class TestImageCaptcha(BaseImageCaptcha):
    kwargs_params = {
        "phrase": False,
        "case": True,
        "numeric": 0,
        "math": False,
        "minLength": 0,
        "maxLength": 0,
        "comment": "None",
        "imgInstructions": "None",
    }
    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in ImageCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in ImageCaptcha.__dict__.keys()
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY

    def test_args(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY

    def test_kwargs(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, **self.kwargs_params)
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    def test_basic_link(self, save_format):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)
        result = instance.captcha_handler(captcha_link=self.captcha_url)

        assert isinstance(result, dict) is True

        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] == 1
            assert result["status"] == "ERROR_CAPTCHA_UNSOLVABLE"

    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    def test_basic_file(self, save_format):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)
        result = instance.captcha_handler(captcha_file=self.captcha_file)

        assert isinstance(result, dict) is True

        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] == 1
            assert result["status"] == "ERROR_CAPTCHA_UNSOLVABLE"

    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    def test_basic_base64(self, save_format):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        with open(self.captcha_file, "rb") as f:
            result = instance.captcha_handler(captcha_base64=f.read())

        assert isinstance(result, dict) is True

        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] == 1
            assert result["status"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    async def test_aio_basic_link(self, save_format):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        result = await instance.aio_captcha_handler(captcha_link=self.captcha_url)
        assert isinstance(result, dict) is True

        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] == 1
            assert result["status"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    async def test_aio_basic_file(self, save_format):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        result = await instance.aio_captcha_handler(captcha_file=self.captcha_file)
        assert isinstance(result, dict) is True

        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] == 1
            assert result["status"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    async def test_aio_basic_base64(self, save_format):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        with open(self.captcha_file, "rb") as f:
            result = await instance.aio_captcha_handler(captcha_base64=f.read())
        assert isinstance(result, dict) is True

        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] == 1
            assert result["status"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    """
    Fail tests
    """

    def test_no_captcha(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = instance.captcha_handler()
        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["solution"]["text"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_no_captcha(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = await instance.aio_captcha_handler()
        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["solution"]["text"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_wrong_link(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = instance.captcha_handler(captcha_link=self.get_random_string(length=50))
        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["solution"]["text"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_wrong_base64(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = instance.captcha_handler(captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8"))
        assert isinstance(result, dict) is True
        assert result["errorId"] == 15
        assert result["taskId"] is None

    @pytest.mark.asyncio
    async def test_aio_wrong_link(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = await instance.aio_captcha_handler(captcha_link=self.get_random_string(length=50))
        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["solution"]["text"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_base64(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = await instance.aio_captcha_handler(
            captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8")
        )
        assert isinstance(result, dict) is True
        assert result["errorId"] == 15
        assert result["taskId"] is None
