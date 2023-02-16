import pytest

from .conftest import CoreTest
from ..python_rucaptcha.core.enums import FunCaptchaEnm
from ..python_rucaptcha.FunCaptcha import FunCaptcha, aioFunCaptcha
from ..python_rucaptcha.serializer import ResponseSer


class TestFuncaptcha(CoreTest):
    publickey = "69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC"
    pageurl = "https://api.funcaptcha.com/fc/api/nojs/"
    surl = "https://client-api.arkoselabs.com"

    """
    Success tests
    """

    def test_basic_data(self):
        instance = FunCaptcha(
            pageurl=self.pageurl,
            publickey=self.publickey,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            surl=self.surl,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == FunCaptchaEnm.FUNCAPTCHA.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["publickey"] == self.publickey
        assert instance.post_payload["surl"] == self.surl

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = aioFunCaptcha(
            pageurl=self.pageurl,
            publickey=self.publickey,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            surl=self.surl,
        )
        assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
        assert instance.post_payload["method"] == FunCaptchaEnm.FUNCAPTCHA.value
        assert instance.post_payload["pageurl"] == self.pageurl
        assert instance.post_payload["publickey"] == self.publickey
        assert instance.post_payload["surl"] == self.surl

        result = await instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_basic_data(self):
        with FunCaptcha(
            pageurl=self.pageurl,
            publickey=self.publickey,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            surl=self.surl,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == FunCaptchaEnm.FUNCAPTCHA.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["publickey"] == self.publickey
            assert instance.post_payload["surl"] == self.surl

            result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is False
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] is None
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with aioFunCaptcha(
            pageurl=self.pageurl,
            publickey=self.publickey,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            surl=self.surl,
        ) as instance:
            assert instance.params.rucaptcha_key == self.RUCAPTCHA_KEY
            assert instance.post_payload["method"] == FunCaptchaEnm.FUNCAPTCHA.value
            assert instance.post_payload["pageurl"] == self.pageurl
            assert instance.post_payload["publickey"] == self.publickey
            assert instance.post_payload["surl"] == self.surl

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

    def test_failed_method(self):
        with pytest.raises(ValueError):
            FunCaptcha(
                pageurl=self.pageurl,
                publickey=self.publickey,
                method=self.get_random_string(5),
                rucaptcha_key=self.RUCAPTCHA_KEY,
                surl=self.surl,
            )

    @pytest.mark.asyncio
    def test_aio_failed_method(self):
        with pytest.raises(ValueError):
            aioFunCaptcha(
                pageurl=self.pageurl,
                publickey=self.publickey,
                method=self.get_random_string(5),
                rucaptcha_key=self.RUCAPTCHA_KEY,
                surl=self.surl,
            )

    @pytest.mark.parametrize("elements", [31, 33])
    def test_failed_key_len(self, elements):
        with pytest.raises(ValueError):
            FunCaptcha(
                pageurl=self.pageurl,
                publickey=self.publickey,
                method=FunCaptchaEnm.FUNCAPTCHA.value,
                rucaptcha_key=self.get_random_string(elements),
                surl=self.surl,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("elements", [31, 33])
    def test_aio_failed_key_len(self, elements):
        with pytest.raises(ValueError):
            aioFunCaptcha(
                pageurl=self.pageurl,
                publickey=self.publickey,
                method=FunCaptchaEnm.FUNCAPTCHA.value,
                rucaptcha_key=self.get_random_string(elements),
                surl=self.surl,
            )

    @pytest.mark.asyncio
    async def test_aio_failed_key(self):
        instance = aioFunCaptcha(
            pageurl=self.pageurl,
            publickey=self.publickey,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.get_random_string(32),
            surl=self.surl,
        )
        result = await instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_KEY_DOES_NOT_EXIST"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_failed_key(self):
        instance = FunCaptcha(
            pageurl=self.pageurl,
            publickey=self.publickey,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.get_random_string(32),
            surl=self.surl,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_KEY_DOES_NOT_EXIST"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_context_aio_failed_key(self):
        async with aioFunCaptcha(
            pageurl=self.pageurl,
            publickey=self.publickey,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.get_random_string(32),
            surl=self.surl,
        ) as instance:
            result = await instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_KEY_DOES_NOT_EXIST"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_failed_key(self):
        with FunCaptcha(
            pageurl=self.pageurl,
            publickey=self.publickey,
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.get_random_string(32),
            surl=self.surl,
        ) as instance:
            result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_KEY_DOES_NOT_EXIST"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_aio_failed_publickey(self):
        instance = aioFunCaptcha(
            pageurl=self.pageurl,
            publickey=self.get_random_string(36),
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            surl=self.surl,
        )
        result = await instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_failed_publickey(self):
        instance = FunCaptcha(
            pageurl=self.pageurl,
            publickey=self.get_random_string(36),
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            surl=self.surl,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    @pytest.mark.asyncio
    async def test_context_aio_failed_publickey(self):
        async with aioFunCaptcha(
            pageurl=self.pageurl,
            publickey=self.get_random_string(36),
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            surl=self.surl,
        ) as instance:
            result = await instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()

    def test_context_failed_publickey(self):
        with FunCaptcha(
            pageurl=self.pageurl,
            publickey=self.get_random_string(36),
            method=FunCaptchaEnm.FUNCAPTCHA.value,
            rucaptcha_key=self.RUCAPTCHA_KEY,
            surl=self.surl,
        ) as instance:
            result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert result["taskId"].isnumeric() is True
        assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert isinstance(result["captchaSolve"], dict) is True
        assert result.keys() == ResponseSer().dict().keys()
