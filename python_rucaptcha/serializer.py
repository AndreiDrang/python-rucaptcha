from uuid import uuid4

from pydantic import Field, BaseModel, validator


class CaptchaOptionsSer(BaseModel):
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


class NormalCaptchaSer(BaseModel):
    method: str = "normal"
    requestId: str = Field(default_factory=uuid4)
    body: str = str()
    options: "CaptchaOptionsSer" = CaptchaOptionsSer()


class TextCaptchaSer(BaseModel):
    method: str = "text"
    requestId: str = Field(default_factory=uuid4)
    body: str = str()
    options: "CaptchaOptionsSer" = CaptchaOptionsSer()


class SocketResponse(BaseModel):
    method: str = str()
    success: bool = None
    code: str = str()
    # captcha task ID at RuCaptcha service
    captchaId: int = -1
    # manually generated requestID
    requestId: str = Field(default_factory=uuid4)
    error: str = str()
    # specific fields for balance request response
    balance: float = 0
    valute: str = str()


class SockAuthSer(BaseModel):
    method: str = "auth"
    requestId: str = Field(default_factory=uuid4)
    key: str
    options: dict
