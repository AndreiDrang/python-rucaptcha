from enum import Enum
from typing import List


class MyEnum(Enum):
    @classmethod
    def list(cls) -> List[Enum]:
        return list(map(lambda c: c, cls))

    @classmethod
    def list_values(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls) -> List[str]:
        return list(map(lambda c: c.name, cls))


class ServicesEnm(MyEnum):
    TWOCAPTCHA = "2captcha"
    RUCAPTCHA = "rucaptcha"


class SaveFormatsEnm(MyEnum):
    TEMP = "temp"
    CONST = "const"


class GeetestEnm(MyEnum):
    GEETEST = "geetest"
    GEETEST_V4 = "geetest_v4"


class ImageCaptchaEnm(MyEnum):
    BASE64 = "base64"


class CapyPuzzleEnm(MyEnum):
    CAPY = "capy"


class FunCaptchaEnm(MyEnum):
    FUNCAPTCHA = "funcaptcha"


class ReCaptchaEnm(MyEnum):
    USER_RECAPTCHA = "userrecaptcha"


class LeminCroppedCaptchaEnm(MyEnum):
    LEMIN = "lemin"


class HCaptchaEnm(MyEnum):
    HCAPTCHA = "hcaptcha"


class KeyCaptchaEnm(MyEnum):
    KEYCAPTCHA = "keycaptcha"


class RotateCaptchaEnm(MyEnum):
    ROTATECAPTCHA = "rotatecaptcha"


class TikTokCaptchaEnm(MyEnum):
    TIKTOK = "tiktok"


class CaptchaControlEnm(MyEnum):
    # default
    GET = "get"
    # https://rucaptcha.com/api-rucaptcha#manage_pingback
    ADD_PINGBACK = "add_pingback"
    GET_PINGBACK = "get_pingback"
    DEL_PINGBACK = "del_pingback"

    # https://rucaptcha.com/api-rucaptcha#additional
    GETBALANCE = "getbalance"
    GET2 = "get2"

    # https://rucaptcha.com/api-rucaptcha#complain
    REPORTGOOD = "reportgood"
    REPORTBAD = "reportbad"


class YandexSmartCaptchaEnm(MyEnum):
    YANDEX = "yandex"


class TurnstileCaptchaEnm(MyEnum):
    TURNSTILE = "turnstile"


class AmazonWAFCaptchaEnm(MyEnum):
    AMAZON_WAF = "amazon_waf"
