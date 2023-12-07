import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import RotateCaptchaEnm
from python_rucaptcha.rotate_captcha import RotateCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestRotateCaptcha(BaseTest):
    captcha_file = "src/examples/rotate/rotate_ex.png"
    captcha_url = "https://rucaptcha.com/dist/web/b771cc7c5eb0c1a811fcb91d54e4443a.png"
    kwargs_params = {
        "angle": 45,
        "comment": "comment comm entcomm entcomment",
    }

    def test_methods_exists(self):
        assert "captcha_handler" in RotateCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in RotateCaptcha.__dict__.keys()

    def test_args(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == RotateCaptchaEnm.RotateTask

    def test_kwargs(self):
        instance = RotateCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    """
    Success tests
    """

    def test_basic_data_link(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = instance.captcha_handler(captcha_link=self.captcha_url)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["rotate"], int) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_basic_data_file(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = instance.captcha_handler(captcha_file=self.captcha_file)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["rotate"], int) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_basic_data_base64(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        with open(self.captcha_file, "rb") as f:
            result = instance.captcha_handler(captcha_base64=f.read())

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["rotate"], int) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data_link(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = await instance.aio_captcha_handler(captcha_link=self.captcha_url)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["rotate"], int) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data_file(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = await instance.aio_captcha_handler(captcha_file=self.captcha_file)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["rotate"], int) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data_base64(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        with open(self.captcha_file, "rb") as f:
            result = await instance.aio_captcha_handler(captcha_base64=f.read())

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["rotate"], int) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    """
    Fail tests
    """

    def test_no_captcha(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["errorId"] != 0
        assert result["taskId"] is None

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_no_captcha(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        assert result["errorId"] != 0
        assert result["taskId"] is None
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_wrong_link(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = instance.captcha_handler(captcha_link=self.get_random_string(length=50))

        assert isinstance(result, dict) is True
        assert result["errorId"] != 0
        assert result["taskId"] is None
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_link(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = await instance.aio_captcha_handler(captcha_link=self.get_random_string(length=50))

        assert isinstance(result, dict) is True
        assert result["errorId"] != 0
        assert result["taskId"] is None
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_wrong_base64(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = instance.captcha_handler(captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8"))

        assert isinstance(result, dict) is True
        assert result["errorId"] != 0
        assert result["taskId"] is None
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_wrong_base64(self):
        instance = RotateCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)

        result = await instance.aio_captcha_handler(
            captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8")
        )

        assert isinstance(result, dict) is True
        assert result["errorId"] != 0
        assert result["taskId"] is None
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()
