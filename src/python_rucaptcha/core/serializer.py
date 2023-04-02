import logging
from uuid import uuid4
from typing import Union, Optional

from pydantic import Field, BaseModel, conint, constr, validator, root_validator

from . import enums
from .config import APP_KEY

"""
Socket API Serializers
"""


class MyBaseModel(BaseModel):
    class Config:
        validate_assignment = True


class CaptchaOptionsSocketSer(MyBaseModel):
    phrase: bool = False
    caseSensitive: bool = False
    numeric: conint(ge=1, le=4) = 0
    calc: bool = False
    minLen: conint(ge=0, le=20) = 0
    maxLen: conint(ge=0, le=20) = 0
    lang: str = ""
    hintText: constr(max_length=139) = ""
    hintImg: str = ""
    softId: str = Field(APP_KEY, const=True)


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


class PostRequestSer(MyBaseModel):
    key: str
    method: str
    soft_id: str = Field(APP_KEY, const=True)
    field_json: int = Field(1, alias="json")


class GetRequestSer(BaseModel):
    key: str
    action: str = "get"
    field_json: int = Field(1, alias="json")

    # Control keys
    ids: str = None
    id: str = None


class CaptchaOptionsSer(BaseModel):
    method: str
    action: str
    sleep_time: conint(gt=5) = 10
    service_type: str = enums.ServiceEnm.TWOCAPTCHA.value
    rucaptcha_key: constr(min_length=1)

    url_request: Optional[str] = None  # /in.php
    url_response: Optional[str] = None  # /res.php

    @validator("rucaptcha_key")
    def rucaptcha_key_check(cls, value, values, **kwargs):
        service_type = values.get("service_type")
        if service_type in (enums.ServiceEnm.RUCAPTCHA, enums.ServiceEnm.TWOCAPTCHA):
            if len(value) != 32:
                raise ValueError(f"Invalid `rucaptcha_key` len, it must be - 32, u send - {len(value)}")
        return value

    @validator("service_type")
    def service_type_check(cls, value):
        if value not in enums.ServiceEnm.list_values():
            logging.warning(
                f"We support only this list of services - '{', '.join(enums.ServiceEnm.list_values())}', u send - '{value}'. "
                f"All other services you use at your own risk"
            )
        return value

    @root_validator
    def urls_set(cls, values):
        """
        Set request \ response URLs if they not set previously
        """
        if not values.get("url_request") and not values.get("url_response"):
            service_type = values.get("service_type")
            if service_type == enums.ServiceEnm.DEATHBYCAPTCHA:
                values.update(
                    {
                        "url_request": f"http://api.{service_type}.com/2captcha/in.php",
                        "url_response": f"http://api.{service_type}.com/2captcha/res.php",
                    }
                )
            else:
                values.update(
                    {
                        "url_request": f"http://{service_type}.com/in.php",
                        "url_response": f"http://{service_type}.com/res.php",
                    }
                )
        return values


"""
HTTP API Response
"""


class ServicePostResponseSer(MyBaseModel):
    status: int
    request: str


class ServiceGetResponseSer(BaseModel):
    status: int
    request: Union[str, dict]

    # ReCaptcha V3 params
    user_check: str = ""
    user_score: str = ""


class ResponseSer(MyBaseModel):
    captchaSolve: Union[dict, str] = {}
    taskId: Optional[int] = None
    error: bool = False
    errorBody: Optional[str] = None
