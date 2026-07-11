import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import CoordinatesCaptchaEnm, YandexSmartCaptchaEnm
from python_rucaptcha.core.serializer import GetTaskResultResponseSer
from python_rucaptcha.yandex_smart_captcha import YandexSmartCaptcha


class TestYandexSmartCaptcha(BaseTest):
    websiteURL = "https://example.com/"
    websiteKey = "Y5Lh0ti..."
    userAgent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    )
    comment = "select objects in the order of the instruction"
    captcha_file = "src/examples/088636.png"
    instruction_file = "src/examples/bounding_box_start.png"
    kwargs_params = {
        "proxyType": "http",
        "proxyAddress": "1.2.3.4",
        "proxyPort": 8080,
    }

    def test_methods_exists(self):
        assert "captcha_handler" in YandexSmartCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in YandexSmartCaptcha.__dict__.keys()

    @pytest.mark.parametrize(
        "method", YandexSmartCaptchaEnm.list_values() + [CoordinatesCaptchaEnm.CoordinatesTask.value]
    )
    def test_args(self, method: str):
        kwargs = {}
        if method == YandexSmartCaptchaEnm.YandexSmartCaptchaTask.value:
            kwargs = {"proxyType": "http", "proxyAddress": "1.2.3.4", "proxyPort": 8080}
        elif method == CoordinatesCaptchaEnm.CoordinatesTask.value:
            kwargs = {"imgType": "smart_captcha", "comment": self.comment}

        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=method,
            **kwargs,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method

    def test_kwargs(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YandexSmartCaptchaEnm.YandexSmartCaptchaTask,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    def test_no_useragent(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YandexSmartCaptchaEnm.YandexSmartCaptchaTaskProxyless,
        )
        assert "userAgent" not in instance.create_task_payload["task"]

    def test_proxy_params_in_payload(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YandexSmartCaptchaEnm.YandexSmartCaptchaTask,
            proxyType="http",
            proxyAddress="1.2.3.4",
            proxyPort=8080,
        )
        assert instance.create_task_payload["task"]["proxyType"] == "http"
        assert instance.create_task_payload["task"]["proxyAddress"] == "1.2.3.4"
        assert instance.create_task_payload["task"]["proxyPort"] == 8080

    def test_missing_proxy_for_proxy_method(self):
        with pytest.raises(ValueError, match="proxyType|proxyAddress|proxyPort"):
            YandexSmartCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                websiteKey=self.websiteKey,
                method=YandexSmartCaptchaEnm.YandexSmartCaptchaTask,
            )

    def test_missing_required_token_fields(self):
        with pytest.raises(ValueError, match="websiteURL and websiteKey"):
            YandexSmartCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                method=YandexSmartCaptchaEnm.YandexSmartCaptchaTaskProxyless,
            )

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            YandexSmartCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                websiteKey=self.websiteKey,
                method=self.get_random_string(5),
            )

    def test_smart_captcha_missing_comment(self):
        with pytest.raises(ValueError, match="comment"):
            YandexSmartCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                method=CoordinatesCaptchaEnm.CoordinatesTask,
                imgType="smart_captcha",
            )

    def test_smart_captcha_with_instructions(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            method=CoordinatesCaptchaEnm.CoordinatesTask,
            imgType="smart_captcha",
            comment=self.comment,
        )
        result = instance.captcha_handler(
            captcha_file=self.captcha_file,
            imgInstructions_file=self.instruction_file,
        )
        assert isinstance(result, dict) is True
        # The handler will attempt to call the API
        # We just verify it constructs without exception and returns a dict

    def test_pazl_smart_captcha_minimal(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            method=CoordinatesCaptchaEnm.CoordinatesTask,
            imgType="pazl_smart_captcha",
        )
        assert instance.create_task_payload["task"]["imgType"] == "pazl_smart_captcha"
        assert "comment" not in instance.create_task_payload["task"]

    """
    Success tests
    """

    def test_basic_data(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YandexSmartCaptchaEnm.YandexSmartCaptchaTaskProxyless.value,
        )

        result = instance.captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] in ("ready", "processing")
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    async def test_aio_basic_data(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YandexSmartCaptchaEnm.YandexSmartCaptchaTaskProxyless.value,
        )

        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict) is True
        if not result["errorId"]:
            assert result["status"] in ("ready", "processing")
            assert isinstance(result["taskId"], int) is True
        else:
            assert result["errorId"] in (1, 12)
            assert result["errorCode"] in ("ERROR_CAPTCHA_UNSOLVABLE", YandexSmartCaptcha.NO_CAPTCHA_ERR)

        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    def test_context_basic_data(self):
        with YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YandexSmartCaptchaEnm.YandexSmartCaptchaTaskProxyless.value,
        ) as instance:
            assert instance

    async def test_context_aio_basic_data(self):
        async with YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            method=YandexSmartCaptchaEnm.YandexSmartCaptchaTaskProxyless.value,
        ) as instance:
            assert instance

    def test_image_with_url(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            method=CoordinatesCaptchaEnm.CoordinatesTask,
            imgType="smart_captcha",
            comment=self.comment,
        )
        result = instance.captcha_handler(
            captcha_link=self.captcha_file,
            imgInstructions_link=self.instruction_file,
        )
        assert isinstance(result, dict) is True

    def test_no_captcha(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            method=CoordinatesCaptchaEnm.CoordinatesTask,
            imgType="pazl_smart_captcha",
        )
        result = instance.captcha_handler()
        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["errorCode"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()

    async def test_aio_no_captcha(self):
        instance = YandexSmartCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            method=CoordinatesCaptchaEnm.CoordinatesTask,
            imgType="pazl_smart_captcha",
        )
        result = await instance.aio_captcha_handler()
        assert isinstance(result, dict) is True
        assert result["errorId"] == 12
        assert isinstance(result["errorCode"], str) is True
        assert result.keys() == GetTaskResultResponseSer().to_dict().keys()
