import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import CyberSiARAEnm
from python_rucaptcha.cyber_siara_captcha import CyberSiARACaptcha


class TestHCaptcha(BaseTest):
    websiteURL = "https://www.pokemoncenter.com/"
    SlideMasterUrlId = "OXR2LVNvCuXykkZbB8KZIfh162sNT8S2"
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

    kwargs_params = {
        "proxyLogin": "user23",
        "proxyPassword": "p4$$w0rd",
        "proxyType": "socks5",
        "proxyAddress": BaseTest.proxyAddress,
        "proxyPort": BaseTest.proxyPort,
    }

    def test_methods_exists(self):
        assert "captcha_handler" in CyberSiARACaptcha.__dict__.keys()
        assert "aio_captcha_handler" in CyberSiARACaptcha.__dict__.keys()

    @pytest.mark.parametrize("method", CyberSiARAEnm.list_values())
    def test_args(self, method: str):
        instance = CyberSiARACaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            SlideMasterUrlId=self.SlideMasterUrlId,
            userAgent=self.userAgent,
            method=method,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == method
        assert instance.create_task_payload["task"]["websiteURL"] == self.websiteURL
        assert instance.create_task_payload["task"]["SlideMasterUrlId"] == self.SlideMasterUrlId
        assert instance.create_task_payload["task"]["userAgent"] == self.userAgent

    def test_kwargs(self):
        instance = CyberSiARACaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            SlideMasterUrlId=self.SlideMasterUrlId,
            userAgent=self.userAgent,
            method=CyberSiARAEnm.AntiCyberSiAraTaskProxyless,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    """
    Fail tests
    """

    def test_no_websiteURL(self):
        with pytest.raises(TypeError):
            CyberSiARACaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                SlideMasterUrlId=self.SlideMasterUrlId,
                userAgent=self.userAgent,
                method=CyberSiARAEnm.AntiCyberSiAraTaskProxyless,
            )

    def test_no_SlideMasterUrlId(self):
        with pytest.raises(TypeError):
            CyberSiARACaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                userAgent=self.userAgent,
                method=CyberSiARAEnm.AntiCyberSiAraTaskProxyless,
            )

    def test_no_userAgent(self):
        with pytest.raises(TypeError):
            CyberSiARACaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                SlideMasterUrlId=self.SlideMasterUrlId,
                method=CyberSiARAEnm.AntiCyberSiAraTaskProxyless,
            )

    def test_wrong_method(self):
        with pytest.raises(ValueError):
            CyberSiARACaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                SlideMasterUrlId=self.SlideMasterUrlId,
                userAgent=self.userAgent,
                method=self.get_random_string(length=5),
            )
