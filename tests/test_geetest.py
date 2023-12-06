import pytest

from tests.conftest import BaseTest
from python_rucaptcha.gee_test import GeeTest
from python_rucaptcha.core.enums import GeetestEnm
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class TestGeeTestBase(BaseTest):
    pageurl = "https://www.geetest.com/en/demo"
    challenge = "1ad03db8aff920037fb8117827eab171"
    gt = "022397c99c9f646f6477822485f30404"
    api_server = "api.geetest.com"


class TestGeeTestCore(TestGeeTestBase):
    pageurl = "https://www.geetest.com/en/demo"
    challenge = "1ad03db8aff920037fb8117827eab171"
    gt = "022397c99c9f646f6477822485f30404"
    api_server = "api.geetest.com"

    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in GeeTest.__dict__.keys()
        assert "aio_captcha_handler" in GeeTest.__dict__.keys()


class TestGeeTest(TestGeeTestBase):
    """
    Success tests
    """

    def test_basic_data(self):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            websiteURL=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        )

        assert instance.create_task_payload["method"] == GeetestEnm.GeeTestTaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["api_server"] == self.api_server
        assert instance.create_task_payload["gt"] == self.gt
        assert instance.create_task_payload["new_captcha"] == 1

        result = instance.captcha_handler(challenge=self.challenge)

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert isinstance(result["taskId"], int) is True
        assert isinstance(result["errorBody"], str) is True
        assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            websiteURL=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        )

        assert instance.create_task_payload["method"] == GeetestEnm.GeeTestTaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["api_server"] == self.api_server
        assert instance.create_task_payload["gt"] == self.gt
        assert instance.create_task_payload["new_captcha"] == 1

        result = await instance.aio_captcha_handler(challenge=self.challenge)

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert isinstance(result["taskId"], int) is True
        assert isinstance(result["errorBody"], str) is True
        assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            websiteURL=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        ) as instance:
            assert instance.create_task_payload["method"] == GeetestEnm.GeeTestTaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["api_server"] == self.api_server
            assert instance.create_task_payload["gt"] == self.gt
            assert instance.create_task_payload["new_captcha"] == 1

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            websiteURL=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        ) as instance:
            assert instance.create_task_payload["method"] == GeetestEnm.GeeTestTaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["api_server"] == self.api_server
            assert instance.create_task_payload["gt"] == self.gt
            assert instance.create_task_payload["new_captcha"] == 1

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            GeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                gt=self.gt,
                websiteURL=self.pageurl,
                api_server=self.api_server,
                method=self.get_random_string(length=5),
            )

    def test_wrong_method_arg(self):
        with pytest.raises(ValueError):
            GeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                api_server=self.api_server,
                method=GeetestEnm.GeeTestTaskProxyless.value,
            )

    def test_empty_challenge(self):
        with pytest.raises(ValueError):
            GeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                gt=self.gt,
                websiteURL=self.pageurl,
                api_server=self.api_server,
                method=GeetestEnm.GeeTestTaskProxyless.value,
            ).captcha_handler()

    @pytest.mark.asyncio
    async def test_empty_challenge_aio(self):
        with pytest.raises(ValueError):
            await GeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                gt=self.gt,
                websiteURL=self.pageurl,
                api_server=self.api_server,
                method=GeetestEnm.GeeTestTaskProxyless.value,
            ).aio_captcha_handler()


class TestGeeTestV4(TestGeeTestBase):
    def test_basic_data(self):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            websiteURL=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        )

        assert instance.create_task_payload["method"] == GeetestEnm.GeeTestTaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["api_server"] == self.api_server
        assert instance.create_task_payload["gt"] == self.gt
        assert instance.create_task_payload["new_captcha"] == 1

        result = instance.captcha_handler(challenge=self.challenge)

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert isinstance(result["taskId"], int) is True
        assert isinstance(result["errorBody"], str) is True
        assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            websiteURL=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        )

        assert instance.create_task_payload["method"] == GeetestEnm.GeeTestTaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["api_server"] == self.api_server
        assert instance.create_task_payload["gt"] == self.gt
        assert instance.create_task_payload["new_captcha"] == 1

        result = await instance.aio_captcha_handler(challenge=self.challenge)

        assert isinstance(result, dict) is True
        assert result["error"] is True
        assert isinstance(result["taskId"], int) is True
        assert isinstance(result["errorBody"], str) is True
        assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            websiteURL=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        ) as instance:
            assert instance.create_task_payload["method"] == GeetestEnm.GeeTestTaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["api_server"] == self.api_server
            assert instance.create_task_payload["gt"] == self.gt
            assert instance.create_task_payload["new_captcha"] == 1

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            websiteURL=self.pageurl,
            api_server=self.api_server,
            new_captcha=1,
        ) as instance:
            assert instance.create_task_payload["method"] == GeetestEnm.GeeTestTaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["api_server"] == self.api_server
            assert instance.create_task_payload["gt"] == self.gt
            assert instance.create_task_payload["new_captcha"] == 1

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            GeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                captcha_id=self.get_random_string(length=5),
                websiteURL=self.pageurl,
                api_server=self.api_server,
                method=self.get_random_string(length=5),
            )

    def test_wrong_method_arg(self):
        with pytest.raises(ValueError):
            GeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                api_server=self.api_server,
                method=GeetestEnm.GeeTestTaskProxyless.value,
            )
