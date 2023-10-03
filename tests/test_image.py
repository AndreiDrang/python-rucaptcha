import pytest

from tests.conftest import BaseTest, DeathByTest
from python_rucaptcha.core.enums import ServiceEnm, SaveFormatsEnm
from python_rucaptcha.image_captcha import ImageCaptcha
from python_rucaptcha.core.serializer import GetTaskResultRequestSer


class BaseImageCaptcha(BaseTest):
    captcha_file = "src/examples/088636.jpg"
    captcha_url = "https://rucaptcha.com/dist/web/99581b9d446a509a0a01954438a5e36a.jpg"


class TestImageCaptcha(BaseImageCaptcha):
    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in ImageCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in ImageCaptcha.__dict__.keys()

    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    def test_basic_link(self, save_format):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
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
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    def test_basic_base64(self, save_format):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

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
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    async def test_aio_basic_link(self, save_format):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)
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
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    async def test_aio_basic_file(self, save_format):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)
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
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    async def test_aio_basic_base64(self, save_format):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

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
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

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
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_no_captcha(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        result = await instance.aio_captcha_handler()
        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == ImageCaptcha.NO_CAPTCHA_ERR
        assert result["captchaSolve"] == {}
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    def test_wrong_link(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        result = instance.captcha_handler(captcha_link=self.get_random_string(length=50))
        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    def test_wrong_base64(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        result = instance.captcha_handler(captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8"))
        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_link(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        result = await instance.aio_captcha_handler(captcha_link=self.get_random_string(length=50))
        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_base64(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        result = await instance.aio_captcha_handler(
            captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8")
        )
        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == GetTaskResultRequestSer().dict().keys()


class TestDeathByImageCaptcha(BaseImageCaptcha, DeathByTest):
    """
    Success tests
    """

    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    def test_basic_data_link(self, save_format):
        instance = ImageCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY, service_type="deathbycaptcha", save_format=save_format
        )

        assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA
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
            assert result["errorBody"] == "ERROR_NO_SLOT_AVAILABLE"

        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    def test_basic_data_file(self, save_format):
        instance = ImageCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY, service_type="deathbycaptcha", save_format=save_format
        )

        assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA
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
            assert result["errorBody"] == "ERROR_NO_SLOT_AVAILABLE"

        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    async def test_aio_basic_data_link(self, save_format):
        instance = ImageCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY, service_type="deathbycaptcha", save_format=save_format
        )

        assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA
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
            assert result["errorBody"] == "ERROR_NO_SLOT_AVAILABLE"

        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("save_format", [SaveFormatsEnm.TEMP, SaveFormatsEnm.CONST])
    async def test_aio_basic_data_file(self, save_format):
        instance = ImageCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY, service_type="deathbycaptcha", save_format=save_format
        )

        assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA
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
            assert result["errorBody"] == "ERROR_NO_SLOT_AVAILABLE"

        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    """
    Fail tests
    """

    def test_no_captcha(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, service_type="deathbycaptcha")

        assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == ImageCaptcha.NO_CAPTCHA_ERR
        assert result["captchaSolve"] == {}

        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_no_captcha(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, service_type="deathbycaptcha")

        assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["errorBody"] == ImageCaptcha.NO_CAPTCHA_ERR
        assert result["captchaSolve"] == {}
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    def test_wrong_link(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, service_type="deathbycaptcha")

        assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = instance.captcha_handler(captcha_link=self.get_random_string(length=50))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == GetTaskResultRequestSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_link(self):
        instance = ImageCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, service_type="deathbycaptcha")

        assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY

        result = await instance.aio_captcha_handler(captcha_link=self.get_random_string(length=50))

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"] is None
        assert result["captchaSolve"] == {}
        assert result.keys() == GetTaskResultRequestSer().dict().keys()
