import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import GridCaptchaEnm, SaveFormatsEnm
from python_rucaptcha.grid_captcha import GridCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestGridCaptcha(BaseTest):
    captcha_file = "src/examples/grid.png"
    kwargs_params = {
        "comment": "None",
        "rows": 3,
        "columns": 3,
        "imgInstructions": "None",
    }
    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in GridCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in GridCaptcha.__dict__.keys()

    @pytest.mark.parametrize("img_clearing", (True, False))
    @pytest.mark.parametrize("save_format", SaveFormatsEnm.list_values())
    def test_args(self, save_format: str, img_clearing: bool):
        instance = GridCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            img_clearing=img_clearing,
            save_format=save_format,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == GridCaptchaEnm.GridTask
        assert instance.save_format == save_format
        assert instance.img_clearing == img_clearing

    def test_kwargs(self):
        instance = GridCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, **self.kwargs_params)
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    @pytest.mark.parametrize("save_format", SaveFormatsEnm.list_values())
    def test_basic_file(self, save_format):
        instance = GridCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)
        result = instance.captcha_handler(captcha_file=self.captcha_file)

        assert isinstance(result, dict) is True

        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"], dict) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

    @pytest.mark.parametrize("save_format", SaveFormatsEnm.list_values())
    def test_basic_base64(self, save_format):
        instance = GridCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        with open(self.captcha_file, "rb") as f:
            result = instance.captcha_handler(captcha_base64=f.read())

        assert isinstance(result, dict) is True

        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"], dict) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.parametrize("save_format", SaveFormatsEnm.list_values())
    async def test_aio_basic_file(self, save_format):
        instance = GridCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        result = await instance.aio_captcha_handler(captcha_file=self.captcha_file)
        assert isinstance(result, dict) is True

        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"], dict) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.parametrize("save_format", SaveFormatsEnm.list_values())
    async def test_aio_basic_base64(self, save_format):
        instance = GridCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY, save_format=save_format)

        with open(self.captcha_file, "rb") as f:
            result = await instance.aio_captcha_handler(captcha_base64=f.read())

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"], dict) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    """
    Fail tests
    """

    def test_no_captcha(self):
        instance = GridCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = instance.captcha_handler()
        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["errorCode"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    async def test_aio_no_captcha(self):
        instance = GridCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = await instance.aio_captcha_handler()
        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["errorCode"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_wrong_link(self):
        instance = GridCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = instance.captcha_handler(captcha_link=self.get_random_string(length=50))
        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["errorCode"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_wrong_base64(self):
        instance = GridCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = instance.captcha_handler(
            captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8")
        )
        assert isinstance(result, dict) is True
        assert result["errorId"] == 15
        assert result["taskId"] is None

    async def test_aio_wrong_link(self):
        instance = GridCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = await instance.aio_captcha_handler(captcha_link=self.get_random_string(length=50))
        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["errorCode"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    async def test_aio_wrong_base64(self):
        instance = GridCaptcha(rucaptcha_key=self.RUCAPTCHA_KEY)
        result = await instance.aio_captcha_handler(
            captcha_base64=self.get_random_string(length=50).encode(encoding="UTF-8")
        )
        assert isinstance(result, dict) is True
        assert result["errorId"] == 15
        assert result["taskId"] is None
