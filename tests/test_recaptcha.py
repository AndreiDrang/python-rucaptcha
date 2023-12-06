import pytest

from tests.conftest import BaseTest, DeathByTest
from python_rucaptcha.core.enums import ServiceEnm, ReCaptchaEnm
from python_rucaptcha.re_captcha import ReCaptcha
from python_rucaptcha.core.serializer import GetTaskResultResponseSer


class BaseReCaptcha(BaseTest):
    googlekey = "6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH"
    pageurl = "https://rucaptcha.com/demo/recaptcha-v2"


class TestReCaptcha(BaseReCaptcha):
    """
    Success tests
    """

    def test_methods_exists(self):
        assert "captcha_handler" in ReCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in ReCaptcha.__dict__.keys()

    def test_basic_data(self):
        instance = ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            googlekey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
        )

        assert instance.create_task_payload["method"] == ReCaptchaEnm.RecaptchaV2TaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["googlekey"] == self.googlekey

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            googlekey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
        )

        assert instance.create_task_payload["method"] == ReCaptchaEnm.RecaptchaV2TaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["googlekey"] == self.googlekey

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            googlekey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
        ) as instance:
            assert instance.create_task_payload["method"] == ReCaptchaEnm.RecaptchaV2TaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["googlekey"] == self.googlekey

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            pageurl=self.pageurl,
            googlekey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
        ) as instance:
            assert instance.create_task_payload["method"] == ReCaptchaEnm.RecaptchaV2TaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["googlekey"] == self.googlekey

    """
    Fail tests
    """

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            ReCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                pageurl=self.pageurl,
                googlekey=self.googlekey,
                method=self.get_random_string(length=5),
            )


class TestDeathByReCaptcha(BaseReCaptcha, DeathByTest):
    """
    Success tests
    """

    def test_basic_data(self):
        instance = ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            service_type="deathbycaptcha",
            pageurl=self.pageurl,
            googlekey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
        )
        assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA

        assert instance.create_task_payload["method"] == ReCaptchaEnm.RecaptchaV2TaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["googlekey"] == self.googlekey

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    @pytest.mark.asyncio
    async def test_aio_basic_data(self):
        instance = ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            service_type="deathbycaptcha",
            pageurl=self.pageurl,
            googlekey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
        )
        assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA

        assert instance.create_task_payload["method"] == ReCaptchaEnm.RecaptchaV2TaskProxyless.value
        assert instance.create_task_payload["pageurl"] == self.pageurl
        assert instance.create_task_payload["googlekey"] == self.googlekey

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if result["error"] is False:
            assert result["error"] is False
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] is None
            assert isinstance(result["captchaSolve"], str) is True
        else:
            assert result["error"] is True
            assert isinstance(result["taskId"], int) is True
            assert result["errorBody"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            service_type="deathbycaptcha",
            pageurl=self.pageurl,
            googlekey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
        ) as instance:
            assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA

            assert instance.create_task_payload["method"] == ReCaptchaEnm.RecaptchaV2TaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["googlekey"] == self.googlekey

    @pytest.mark.asyncio
    async def test_context_aio_basic_data(self):
        async with ReCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            service_type="deathbycaptcha",
            pageurl=self.pageurl,
            googlekey=self.googlekey,
            method=ReCaptchaEnm.RecaptchaV2TaskProxyless.value,
        ) as instance:
            assert instance.params.service_type == ServiceEnm.DEATHBYCAPTCHA

            assert instance.create_task_payload["method"] == ReCaptchaEnm.RecaptchaV2TaskProxyless.value
            assert instance.create_task_payload["pageurl"] == self.pageurl
            assert instance.create_task_payload["googlekey"] == self.googlekey
