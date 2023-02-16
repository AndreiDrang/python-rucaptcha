import pytest

from .conftest import CoreTest
from ..python_rucaptcha.core.enums import CapyPuzzleEnm
from ..python_rucaptcha.CapyPuzzle import CapyPuzzle, aioCapyPuzzle
from core.serializer import ResponseSer


class TestCapyPuzzle(CoreTest):
    captchakey = "PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w"
    pageurl = "https://www.capy.me/account/register/"
    api_server = "https://jp.api.capy.me/"
    versions = ["puzzle", "avatar"]

    """
    Success tests
    """

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
        instance = aioCapyPuzzle(
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

        result = await instance.captcha_handler()

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
        async with aioCapyPuzzle(
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

            result = await instance.captcha_handler()

            assert isinstance(result, dict) is True
            assert result["error"] is False
            assert result["taskId"].isnumeric() is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], dict) is True
            assert result.keys() == ResponseSer().dict().keys()

    """
    Failed tests
    """

    @pytest.mark.parametrize("version", versions)
    def test_failed_capypuzzle_method(self, version):
        with pytest.raises(ValueError):
            CapyPuzzle(
                pageurl=self.pageurl,
                captchakey=self.captchakey,
                method=self.get_random_string(5),
                rucaptcha_key=self.RUCAPTCHA_KEY,
                api_server=self.api_server,
                version=version,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("version", versions)
    def test_aio_failed_capypuzzle_method(self, version):
        with pytest.raises(ValueError):
            aioCapyPuzzle(
                pageurl=self.pageurl,
                captchakey=self.captchakey,
                method=self.get_random_string(5),
                rucaptcha_key=self.RUCAPTCHA_KEY,
                api_server=self.api_server,
                version=version,
            )

    @pytest.mark.parametrize("elements", [31, 33])
    @pytest.mark.parametrize("version", versions)
    def test_failed_capypuzzle_key_len(self, elements, version):
        with pytest.raises(ValueError):
            CapyPuzzle(
                pageurl=self.pageurl,
                captchakey=self.captchakey,
                method=CapyPuzzleEnm.CAPY.value,
                rucaptcha_key=self.get_random_string(elements),
                api_server=self.api_server,
                version=version,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("elements", [31, 33])
    @pytest.mark.parametrize("version", versions)
    def test_aio_failed_capypuzzle_key_len(self, elements, version):
        with pytest.raises(ValueError):
            aioCapyPuzzle(
                pageurl=self.pageurl,
                captchakey=self.captchakey,
                method=CapyPuzzleEnm.CAPY.value,
                rucaptcha_key=self.get_random_string(elements),
                api_server=self.api_server,
                version=version,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("version", versions)
    async def test_aio_failed_capypuzzle_key(self, version):
        instance = aioCapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CAPY.value,
            rucaptcha_key=self.get_random_string(32),
            api_server=self.api_server,
            version=version,
        )
        result = await instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_KEY_DOES_NOT_EXIST"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.parametrize("version", versions)
    def test_failed_capypuzzle_key(self, version):
        instance = CapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CAPY.value,
            rucaptcha_key=self.get_random_string(32),
            api_server=self.api_server,
            version=version,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_KEY_DOES_NOT_EXIST"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("version", versions)
    async def test_context_aio_failed_capypuzzle_key(self, version):
        async with aioCapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CAPY.value,
            rucaptcha_key=self.get_random_string(32),
            api_server=self.api_server,
            version=version,
        ) as instance:
            result = await instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_KEY_DOES_NOT_EXIST"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.parametrize("version", versions)
    def test_context_failed_capypuzzle_key(self, version):
        with CapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CAPY.value,
            rucaptcha_key=self.get_random_string(32),
            api_server=self.api_server,
            version=version,
        ) as instance:
            result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_KEY_DOES_NOT_EXIST"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()
