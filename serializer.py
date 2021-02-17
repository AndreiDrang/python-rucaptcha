from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from pydantic import BaseModel, ValidationError, validator

from uuid import uuid4


class CaptchaOptions(BaseModel):
    phrase: bool = False
    caseSensitive: bool = False
    numeric: int = 0
    calc: bool = False
    minLen: int = 0
    maxLen: int = 0
    lang: str = ""
    hintText: str = ""
    hintImg: str = ""
    softId: str = "1899"

    @validator("numeric")
    def numeric_check(cls, value):
        if value not in range(1, 5):
            raise ValueError("Invalid `numeric` param value")
        return value

    @validator("minLen", "maxLen")
    def len_check(cls, value):
        if value not in range(0, 21):
            raise ValueError("Invalid `minLen \ maxLen` param value")
        return value

    @validator("hintText")
    def hint_text_check(cls, value):
        if len(value) > 140:
            raise ValueError("Invalid `hintText` param value")
        return value

    @validator("softId")
    def soft_id_set(cls, value):
        value.update({"softId": "1899"})
        return value


class NormalCaptcha(BaseModel):
    method: str = "normal"
    requestId: str = uuid4()
    body: str
    options: "CaptchaOptions" = CaptchaOptions()
