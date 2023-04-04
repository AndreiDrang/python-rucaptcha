import pytest

from tests.conftest import BaseTest
from python_rucaptcha.rotate_captcha import RotateCaptcha
from python_rucaptcha.core.serializer import ResponseSer


class TestRotateCaptcha(BaseTest):
    captcha_file = "src/examples/rotate/rotate_ex.png"
    captcha_url = "https://rucaptcha.com/dist/web/b771cc7c5eb0c1a811fcb91d54e4443a.png"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in RotateCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in RotateCaptcha.__dict__.keys()

    def test_basic_data_link(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(captcha_link=self.captcha_url)

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

    def test_basic_data_file(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

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

    def test_basic_data_base64(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        with open(self.captcha_file, "rb") as f:
            result = instance.captcha_handler(captcha_base64=f.read())

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
    async def test_aio_basic_data_link(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler(captcha_link=self.captcha_url)

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
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

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
    async def test_aio_basic_data_base64(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        with open(self.captcha_file, "rb") as f:
            result = await instance.aio_captcha_handler(captcha_base64=f.read())

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

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, method=self.get_random_string(length=5))

    def test_no_captcha(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == RotateCaptcha.NO_CAPTCHA_ERR
        assert result["captchaSolve"] == {}

        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_no_captcha(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == RotateCaptcha.NO_CAPTCHA_ERR
        assert result["captchaSolve"] == {}
        assert result.keys() == ResponseSer().dict().keys()

    def test_wrong_link(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(captcha_link=self.get_random_string(length=50))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == ResponseSer().dict().keys()

    def test_wrong_base64(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8"))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_link(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler(captcha_link=self.get_random_string(length=50))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_base64(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler(
            captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8")
        )

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == ResponseSer().dict().keys()
