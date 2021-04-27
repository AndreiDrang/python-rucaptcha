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
