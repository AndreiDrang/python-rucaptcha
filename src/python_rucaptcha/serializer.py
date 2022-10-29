from uuid import uuid4
from typing import Union

from pydantic import Field, BaseModel, conint, constr, validator, root_validator

from . import enums
from .config import APP_KEY

"""
Socket API Serializers
"""


class CaptchaOptionsSocketSer(BaseModel):
    phrase: bool = False
    caseSensitive: bool = False
    numeric: conint(ge=1, le=4) = 0
    calc: bool = False
    minLen: conint(ge=0, le=20) = 0
    maxLen: conint(ge=0, le=20) = 0
    lang: str = ""
    hintText: constr(max_length=139) = ""
    hintImg: str = ""
    softId: str = "1899"

    @validator("hintText")
    def hint_text_check(cls, value):
        if len(value) > 140:
            raise ValueError("Invalid `hintText` param value")
        return value

    @validator("softId")
    def soft_id_set(cls, value):
        value.update({"softId": "1899"})
        return value


class NormalCaptchaSocketSer(BaseModel):
    method: str = "normal"
    requestId: str = Field(default_factory=lambda: str(uuid4()))
    body: str = str()
    options: "CaptchaOptionsSocketSer" = CaptchaOptionsSocketSer()


class TextCaptchaSocketSer(BaseModel):
    method: str = "text"
    requestId: str = Field(default_factory=lambda: str(uuid4()))
    body: str = str()
    options: "CaptchaOptionsSocketSer" = CaptchaOptionsSocketSer()


class ControlCaptchaSocketSer(BaseModel):
    method: str
    requestId: str = Field(default_factory=lambda: str(uuid4()))
    success: str = None
    captchaId: int = None


class SocketResponse(BaseModel):
    method: str = None
    success: bool = None
    code: str = None
    # captcha task ID at RuCaptcha service
    captchaId: int = None
    # manually generated requestID
    requestId: str = Field(default_factory=lambda: str(uuid4()))
    error: str = None
    # specific fields for balance request response
    balance: float = None
    valute: str = None


class SockAuthSer(BaseModel):
    method: str = "auth"
    requestId: str = Field(default_factory=lambda: str(uuid4()))
    key: str
    options: dict


"""
HTTP API Serializers
"""


class PostRequestSer(BaseModel):
    key: str
    method: str
    soft_id: str = APP_KEY
    field_json: int = Field(1, alias="json")


class GetRequestSer(BaseModel):
    key: str
    action: str = "get"
    field_json: int = Field(1, alias="json")

    # Control keys
    ids: str = None
    id: str = None


class CaptchaOptionsSer(BaseModel):
    rucaptcha_key: constr(min_length=32, max_length=32)
    method: str
    action: str
    sleep_time: conint(gt=5) = 10
    service_type: str = enums.ServicesEnm.TWOCAPTCHA.value

    # CaptchaImage
    # save_format: str = enums.SaveFormatsEnm.TEMP.value
    # img_clearing: bool = True
    # img_path: str = "PythonRuCaptchaImages"

    url_request: str = ""
    url_response: str = ""

    @validator("service_type")
    def service_type_check(cls, value):
        if value not in enums.ServicesEnm.list_values():
            raise ValueError(
                f"Invalid `service_type`, valid params - {','.join(enums.ServicesEnm.list_values())}, send - {value}"
            )
        return value

    @root_validator
    def urls_set(cls, values):
        service_type = values.get("service_type")
        values.update(
            {"url_request": f"http://{service_type}.com/in.php", "url_response": f"http://{service_type}.com/res.php"}
        )
        return values


"""
HTTP API Response
"""


class ServicePostResponseSer(BaseModel):
    status: int
    request: str


class ServiceGetResponseSer(BaseModel):
    status: int
    request: Union[str, dict]

    # ReCaptcha V3 params
    user_check: str = ""
    user_score: str = ""


class ResponseSer(BaseModel):
    serverAnswer: dict = {}
    captchaSolve: dict = {}
    taskId: int = None
    error: bool = False
    errorBody: str = None

    @validator("taskId", pre=True, always=True)
    def dt_check(cls, value):
        if value:
            value = int(value)
        return value
