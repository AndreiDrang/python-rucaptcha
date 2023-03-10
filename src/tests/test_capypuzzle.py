import pytest

from src.tests.conftest import BaseTest
from python_rucaptcha.core.enums import CapyPuzzleEnm
from python_rucaptcha.capy_puzzle import CapyPuzzle
from python_rucaptcha.core.serializer import ResponseSer


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

    def test_capypuzzle_basic_data(self):
        instance = CapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CAPY.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            api_server=self.api_server,
            version=self.versions[0],
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == CapyPuzzleEnm.CAPY.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["api_server"] == self.api_server
        assert instance.post_payload["version"] == self.versions[0]

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_capypuzzle_basic_data(self):
        instance = CapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CAPY.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            api_server=self.api_server,
            version=self.versions[0],
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == CapyPuzzleEnm.CAPY.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["api_server"] == self.api_server
        assert instance.post_payload["version"] == self.versions[0]

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_capypuzzle_basic_data(self):
        with CapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CAPY.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            api_server=self.api_server,
            version=self.versions[0],
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == CapyPuzzleEnm.CAPY.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["api_server"] == self.api_server
            assert instance.post_payload["version"] == self.versions[0]

            result = instance.captcha_handler()

            assert isinstance(result, dict) is True
            assert result["error"] is False
            assert result["taskId"].isnumeric() is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], dict) is True
            assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_context_aio_capypuzzle_basic_data(self):
        async with CapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CAPY.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            api_server=self.api_server,
            version=self.versions[0],
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == CapyPuzzleEnm.CAPY.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["api_server"] == self.api_server
            assert instance.post_payload["version"] == self.versions[0]

            result = await instance.aio_captcha_handler()

            assert isinstance(result, dict) is True
            assert result["error"] is False
            assert result["taskId"].isnumeric() is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], dict) is True
            assert result.keys() == ResponseSer().dict().keys()

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
