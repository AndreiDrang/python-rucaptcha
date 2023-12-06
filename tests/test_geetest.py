import pytest

from tests.conftest import BaseTest
from python_rucaptcha.gee_test import GeeTest
from python_rucaptcha.core.enums import GeetestEnm


class TestGeeTestBase(BaseTest):
    pageurl = "https://www.geetest.com/en/demo"
    challenge = "1ad03db8aff920037fb8117827eab171"
    gt = "022397c99c9f646f6477822485f30404"
    api_server = "api.geetest.com"


class TestGeeTestCore(TestGeeTestBase):
    kwargs_params = {
        "geetestApiServerSubdomain": "api-na.geetest.com",
        "userAgent": "Some specific user agent",
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }
    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in GeeTest.__dict__.keys()
        assert "aio_captcha_handler" in GeeTest.__dict__.keys()

    @pytest.mark.parametrize("method", GeetestEnm.GeeTestTaskProxyless.list_values())
    def test_args(self, method: str):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            method=method,
            gt=self.gt,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.pageurl
        assert instance.create_task_payload["task"]["gt"] == self.gt

    def test_kwargs(self):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            gt=self.gt,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))


class TestGeeTest(TestGeeTestBase):
    """
    Success tests
    """

    def test_basic_data(self):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            gt=self.gt,
        )

        result = instance.captcha_handler(challenge=self.challenge)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

    async def test_aio_basic_data(self):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            gt=self.gt,
        )

        result = await instance.aio_captcha_handler(challenge=self.challenge)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

    def test_context_basic_data(self):
        with GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            gt=self.gt,
        ) as instance:
            assert instance.captcha_handler(challenge=self.challenge)

    async def test_context_aio_basic_data(self):
        async with GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.pageurl,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            gt=self.gt,
        ) as instance:
            assert await instance.aio_captcha_handler(challenge=self.challenge)

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
        with pytest.raises(TypeError):
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
            websiteURL=self.pageurl,
            api_server=self.api_server,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            version=4,
            initParameters={"captcha_id": "e392e1d7fd421dc63325744d5a2b9c73"},
        )
        result = instance.captcha_handler(challenge=self.challenge)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            websiteURL=self.pageurl,
            api_server=self.api_server,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            version=4,
            initParameters={"captcha_id": "e392e1d7fd421dc63325744d5a2b9c73"},
        )
        result = await instance.aio_captcha_handler(challenge=self.challenge)

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] == "ready"
            assert isinstance(result["solution"]["text"], str) is True
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

    def test_context_basic_data(self):
        with GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            websiteURL=self.pageurl,
            api_server=self.api_server,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            version=4,
            initParameters={"captcha_id": "e392e1d7fd421dc63325744d5a2b9c73"},
        ) as instance:
            assert instance.captcha_handler(challenge=self.challenge)

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with GeeTest(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            gt=self.gt,
            websiteURL=self.pageurl,
            api_server=self.api_server,
            method=GeetestEnm.GeeTestTaskProxyless.value,
            version=4,
            initParameters={"captcha_id": "e392e1d7fd421dc63325744d5a2b9c73"},
        ) as instance:
            assert await instance.aio_captcha_handler(challenge=self.challenge)

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
                version=4,
                initParameters={"captcha_id": "e392e1d7fd421dc63325744d5a2b9c73"},
            )

    def test_wrong_method_arg(self):
        with pytest.raises(TypeError):
            GeeTest(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.pageurl,
                api_server=self.api_server,
                method=GeetestEnm.GeeTestTaskProxyless.value,
                version=4,
                initParameters={"captcha_id": "e392e1d7fd421dc63325744d5a2b9c73"},
            )
