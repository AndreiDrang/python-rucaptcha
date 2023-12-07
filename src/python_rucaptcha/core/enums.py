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
    GeeTestTask = "GeeTestTask"
    GeeTestTaskProxyless = "GeeTestTaskProxyless"


class ImageCaptchaEnm(str, MyEnum):
    ImageToTextTask = "ImageToTextTask"


class CapyPuzzleEnm(str, MyEnum):
    CapyTask = "CapyTask"
    CapyTaskProxyless = "CapyTaskProxyless"


class FunCaptchaEnm(str, MyEnum):
    FunCaptchaTaskProxyless = "FunCaptchaTaskProxyless"
    FunCaptchaTask = "FunCaptchaTask"


class ReCaptchaEnm(str, MyEnum):
    RecaptchaV2TaskProxyless = "RecaptchaV2TaskProxyless"
    RecaptchaV2Task = "RecaptchaV2Task"

    RecaptchaV2EnterpriseTaskProxyless = "RecaptchaV2EnterpriseTaskProxyless"
    RecaptchaV2EnterpriseTask = "RecaptchaV2EnterpriseTask"

    RecaptchaV3TaskProxyless = "RecaptchaV3TaskProxyless"


class LeminCaptchaEnm(str, MyEnum):
    LeminTaskProxyless = "LeminTaskProxyless"
    LeminTask = "LeminTask"


class HCaptchaEnm(str, MyEnum):
    HCaptchaTask = "HCaptchaTask"
    HCaptchaTaskProxyless = "HCaptchaTaskProxyless"


class KeyCaptchaEnm(str, MyEnum):
    KeyCaptchaTask = "KeyCaptchaTask"
    KeyCaptchaTaskProxyless = "KeyCaptchaTaskProxyless"


class RotateCaptchaEnm(str, MyEnum):
    RotateTask = "RotateTask"


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


class TurnstileCaptchaEnm(str, MyEnum):
    TurnstileTaskProxyless = "TurnstileTaskProxyless"
    TurnstileTask = "TurnstileTask"


class AmazonWAFCaptchaEnm(str, MyEnum):
    AmazonTask = "AmazonTask"
    AmazonTaskProxyless = "AmazonTaskProxyless"


class TextCaptchaEnm(str, MyEnum):
    TextCaptchaTask = "TextCaptchaTask"


class AudioCaptchaEnm(str, MyEnum):
    AudioTask = "AudioTask"
