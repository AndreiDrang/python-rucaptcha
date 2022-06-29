import pytest

from .conftest import CoreTest
from ..python_rucaptcha.enums import CapyPuzzleEnm
from ..python_rucaptcha.CapyPuzzle import CapyPuzzle, aioCapyPuzzle
from ..python_rucaptcha.serializer import ResponseSer


class TestCapyPuzzle(CoreTest):
    captchakey = "PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w"
    pageurl = "https://www.capy.me/account/register/"
    api_server = "https://jp.api.capy.me/"
    versions = ["puzzle", "avatar"]

    """
    Success tests
    """

    @pytest.mark.parametrize("version", versions)
    def test_capypuzzle_basic_data(self, version):
        instance = CapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CAPY.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            api_server=self.api_server,
            version=version,
        )
        assert instance.params.method == CapyPuzzleEnm.CAPY.value
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["api_server"] == self.api_server
        assert instance.post_payload["version"] == version

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric()
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("version", versions)
    async def test_aio_capypuzzle_basic_data(self, version):
        instance = aioCapyPuzzle(
            pageurl=self.pageurl,
            captchakey=self.captchakey,
            method=CapyPuzzleEnm.CAPY.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            api_server=self.api_server,
            version=version,
        )
        assert instance.params.method == CapyPuzzleEnm.CAPY.value
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["api_server"] == self.api_server
        assert instance.post_payload["version"] == version

        result = await instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric()
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
