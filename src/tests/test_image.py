import pytest

from src.tests.conftest import BaseTest
from python_rucaptcha.core.enums import SaveFormatsEnm
from python_rucaptcha.image_captcha import ImageCaptcha
from python_rucaptcha.core.serializer import ResponseSer


class TestImageCaptcha(BaseTest):
    captcha_file = "examples/088636.png"
    captcha_url = "https://rucaptcha.com/dist/web/99581b9d446a509a0a01954438a5e36a.jpg"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in ImageCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in ImageCaptcha.__dict__.keys()

    def test_basic_data_link(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(captcha_link=self.captcha_url)

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

    def test_basic_data_link_const(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=SaveFormatsEnm.CONST)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(captcha_link=self.captcha_url)

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

    def test_basic_data_file(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(captcha_file=self.captcha_file)

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

    def test_basic_data_file_const(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=SaveFormatsEnm.CONST)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(captcha_file=self.captcha_file)

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
    async def test_aio_basic_data_link(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler(captcha_link=self.captcha_url)

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
    async def test_aio_basic_data_file(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler(captcha_file=self.captcha_file)

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

    def test_no_captcha(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == ImageCaptcha.NO_CAPTCHA_ERR
        assert result["captchaSolve"] == {}

        assert result.keys() == ResponseSer().dict().keys()
