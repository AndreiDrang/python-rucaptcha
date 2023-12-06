from enum import Enum
from typing import List


class MyEnum(Enum):
    """
    Base class for work with updated Enums
    """

    @classmethod
    def list(cls) -> List[Enum]:
        return list(map(lambda c: c, cls))

    @classmethod
    def list_values(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls) -> List[str]:
        return list(map(lambda c: c.name, cls))


class ServiceEnm(str, MyEnum):
    TWOCAPTCHA = "2captcha"
    RUCAPTCHA = "rucaptcha"
    DEATHBYCAPTCHA = "deathbycaptcha"


class SaveFormatsEnm(str, MyEnum):
    TEMP = "temp"
    CONST = "const"


class GeetestEnm(str, MyEnum):
    GEETEST = "geetest"
    GEETEST_V4 = "geetest_v4"


class ImageCaptchaEnm(str, MyEnum):
    ImageToTextTask = "ImageToTextTask"


class CapyPuzzleEnm(str, MyEnum):
    CAPY = "capy"


class FunCaptchaEnm(str, MyEnum):
    FUNCAPTCHA = "funcaptcha"


class ReCaptchaEnm(str, MyEnum):
    USER_RECAPTCHA = "userrecaptcha"


class LeminCroppedCaptchaEnm(str, MyEnum):
    LEMIN = "lemin"


class HCaptchaEnm(str, MyEnum):
    HCAPTCHA = "hcaptcha"


class KeyCaptchaEnm(str, MyEnum):
    KEYCAPTCHA = "keycaptcha"


class RotateCaptchaEnm(str, MyEnum):
    ROTATECAPTCHA = "rotatecaptcha"


class TikTokCaptchaEnm(str, MyEnum):
    TIKTOK = "tiktok"


class ControlEnm(str, MyEnum):
    control = "control"
    # https://rucaptcha.com/api-docs/get-balance
    getBalance = "getBalance"
    # https://rucaptcha.com/api-docs/report-correct
    reportCorrect = "reportCorrect"
    # https://rucaptcha.com/api-docs/report-incorrect
    reportIncorrect = "reportIncorrect"


class YandexSmartCaptchaEnm(str, MyEnum):
    YANDEX = "yandex"


class TurnstileCaptchaEnm(str, MyEnum):
    TURNSTILE = "turnstile"
    TurnstileTaskProxyless = "TurnstileTaskProxyless"
    TurnstileTask = "TurnstileTask"


class AmazonWAFCaptchaEnm(str, MyEnum):
    AmazonTask = "AmazonTask"
    AmazonTaskProxyless = "AmazonTaskProxyless"


class TextCaptchaEnm(str, MyEnum):
    TextCaptchaTask = "TextCaptchaTask"


class AudioCaptchaEnm(str, MyEnum):
    AUDIO = "audio"
