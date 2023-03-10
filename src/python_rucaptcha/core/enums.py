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


class ServicesEnm(str, MyEnum):
    TWOCAPTCHA = "2captcha"
    RUCAPTCHA = "rucaptcha"


class SaveFormatsEnm(str, MyEnum):
    TEMP = "temp"
    CONST = "const"


class GeetestEnm(str, MyEnum):
    GEETEST = "geetest"
    GEETEST_V4 = "geetest_v4"


class ImageCaptchaEnm(str, MyEnum):
    BASE64 = "base64"


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


class YandexSmartCaptchaEnm(str, MyEnum):
    YANDEX = "yandex"


class TurnstileCaptchaEnm(str, MyEnum):
    TURNSTILE = "turnstile"


class AmazonWAFCaptchaEnm(str, MyEnum):
    AMAZON_WAF = "amazon_waf"
