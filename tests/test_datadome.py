import pytest

from tests.conftest import BaseTest
from python_rucaptcha.core.enums import DataDomeSliderEnm
from python_rucaptcha.datadome_captcha import DataDomeCaptcha


class TestHCaptcha(BaseTest):
    websiteURL = "https://www.pokemoncenter.com/"
    captchaUrl = "https://geo.captcha-delivery.com/captcha/?initialCid=AHrlqAAAAAMAlk-FmAyNOW8AUyTH_g%3D%3D&hash=5B45875B653A484CC79E57036CE9FC&cid=noJuZstmvINksqOxaXWQogbPBd01y3VaH3r-CZ4eqK4roZuelJMHVhO2rR0IySRieoAivkg74B4UpJ.xj.jVNB6-aLaW.Bwvik7__EncryD6COavwx8RmOqgZ7DK_3v&t=fe&referer=https%3A%2F%2Fwww.pokemoncenter.com%2F&s=9817&e=2b1d5a78107ded0dcdc8317aa879979ed5083a2b3a95b734dbe7871679e1403"
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    proxyType = "http"
    proxyAddress = "1.2.3.4"
    proxyPort = "8080"
    kwargs_params = {"proxyLogin": "user23", "proxyPassword": "p4$$w0rd"}

    def test_methods_exists(self):
        assert "captcha_handler" in DataDomeCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in DataDomeCaptcha.__dict__.keys()

    def test_args(self):
        instance = DataDomeCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            captchaUrl=self.captchaUrl,
            userAgent=self.userAgent,
            proxyType=self.proxyType,
            proxyAddress=self.proxyAddress,
            proxyPort=self.proxyPort,
        )
        assert instance.create_task_payload["clientKey"] == self.RUCAPTCHA_KEY
        assert instance.create_task_payload["task"]["type"] == DataDomeSliderEnm.DataDomeSliderTask
        assert instance.create_task_payload["task"]["websiteURL"] == self.websiteURL
        assert instance.create_task_payload["task"]["captchaUrl"] == self.captchaUrl
        assert instance.create_task_payload["task"]["userAgent"] == self.userAgent
        assert instance.create_task_payload["task"]["proxyType"] == self.proxyType
        assert instance.create_task_payload["task"]["proxyAddress"] == self.proxyAddress
        assert instance.create_task_payload["task"]["proxyPort"] == self.proxyPort

    def test_kwargs(self):
        instance = DataDomeCaptcha(
            rucaptcha_key=self.RUCAPTCHA_KEY,
            websiteURL=self.websiteURL,
            captchaUrl=self.captchaUrl,
            userAgent=self.userAgent,
            proxyType=self.proxyType,
            proxyAddress=self.proxyAddress,
            proxyPort=self.proxyPort,
            **self.kwargs_params,
        )
        assert set(self.kwargs_params.keys()).issubset(set(instance.create_task_payload["task"].keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.create_task_payload["task"].values()))

    """
    Fail tests
    """

    def test_no_websiteURL(self):
        with pytest.raises(TypeError):
            DataDomeCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                captchaUrl=self.captchaUrl,
                userAgent=self.userAgent,
                proxyType=self.proxyType,
                proxyAddress=self.proxyAddress,
                proxyPort=self.proxyPort,
            )

    def test_no_captchaUrl(self):
        with pytest.raises(TypeError):
            DataDomeCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                userAgent=self.userAgent,
                proxyType=self.proxyType,
                proxyAddress=self.proxyAddress,
                proxyPort=self.proxyPort,
            )

    def test_no_userAgent(self):
        with pytest.raises(TypeError):
            DataDomeCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                captchaUrl=self.captchaUrl,
                proxyType=self.proxyType,
                proxyAddress=self.proxyAddress,
                proxyPort=self.proxyPort,
            )

    def test_no_proxyType(self):
        with pytest.raises(TypeError):
            DataDomeCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                captchaUrl=self.captchaUrl,
                userAgent=self.userAgent,
                proxyAddress=self.proxyAddress,
                proxyPort=self.proxyPort,
            )

    def test_no_proxyAddress(self):
        with pytest.raises(TypeError):
            DataDomeCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                captchaUrl=self.captchaUrl,
                userAgent=self.userAgent,
                proxyType=self.proxyType,
                proxyPort=self.proxyPort,
            )

    def test_no_proxyPort(self):
        with pytest.raises(TypeError):
            DataDomeCaptcha(
                rucaptcha_key=self.RUCAPTCHA_KEY,
                websiteURL=self.websiteURL,
                captchaUrl=self.captchaUrl,
                userAgent=self.userAgent,
                proxyType=self.proxyType,
                proxyAddress=self.proxyAddress,
            )
