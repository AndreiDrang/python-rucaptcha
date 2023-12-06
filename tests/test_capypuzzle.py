import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import CapyPuzzleEnm
from python_rucaptcha.capy_puzzle import CapyPuzzle
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestCapyPuzzle(BaseTest):
    captchakey = "PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w"
    pageurl = "https://www.capy.me/account/register/"
    api_server = "https://jp.api.capy.me/"
    versions = ["puzzle", "avatar"]

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in CapyPuzzle.__dict__.keys()
        assert "aio_captcha_handler" in CapyPuzzle.__dict__.keys()

    def test_basic_data(self):
        instance = CapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CapyTaskProxyless.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            api_server=self.api_server,
            version=self.versions[0],
        )
        assert instance.create_task_payload["method"] == CapyPuzzleEnm.CapyTaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["api_server"] == self.api_server
        assert instance.create_task_payload["version"] == self.versions[0]

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = CapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CapyTaskProxyless.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            api_server=self.api_server,
            version=self.versions[0],
        )
        assert instance.create_task_payload["method"] == CapyPuzzleEnm.CapyTaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["api_server"] == self.api_server
        assert instance.create_task_payload["version"] == self.versions[0]

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with CapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CapyTaskProxyless.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            api_server=self.api_server,
            version=self.versions[0],
        ) as instance:
            assert instance.create_task_payload["method"] == CapyPuzzleEnm.CapyTaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["api_server"] == self.api_server
            assert instance.create_task_payload["version"] == self.versions[0]

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with CapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CapyTaskProxyless.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            api_server=self.api_server,
            version=self.versions[0],
        ) as instance:
            assert instance.create_task_payload["method"] == CapyPuzzleEnm.CapyTaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["api_server"] == self.api_server
            assert instance.create_task_payload["version"] == self.versions[0]

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            CapyPuzzle(
                pageurl=self.pageurl,
                captchakey=self.captchakey,
                method=self.get_random_string(length=5),
                rucaptcha_key=self.RUCAPTCHA_KEY,
            )
