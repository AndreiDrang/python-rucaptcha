from typing import Any, Literal
from decimal import Decimal
from datetime import date, datetime

from msgspec import Struct

from . import enums
from .config import APP_KEY


class MyBaseModel(Struct):
    def to_dict(self) -> dict[str, Any]:
        result = {}
        for field in self.__struct_fields__:
            value = getattr(self, field)

            if isinstance(value, MyBaseModel):
                result[field] = value.to_dict()

            elif isinstance(value, (list, tuple)) and all(isinstance(el, Struct) for el in value):
                result[field] = [el.to_dict() for el in value]

            elif isinstance(value, (date, datetime)):
                result[field] = value.isoformat()

            elif isinstance(value, Decimal):
                result[field] = str(value)

            else:
                result[field] = value

        return result


"""
HTTP API Serializers
"""


class TaskSer(MyBaseModel):
    type: str


class CreateTaskBaseSer(MyBaseModel):
    clientKey: str
    task: TaskSer
    languagePool: str = "en"
    callbackUrl: str | None = None
    soft_id: Literal[APP_KEY] = APP_KEY


class GetTaskResultRequestSer(MyBaseModel):
    clientKey: str
    taskId: int | None = None


class CaptchaOptionsSer(MyBaseModel):
    sleep_time: int = 10
    service_type: enums.ServiceEnm | str = enums.ServiceEnm.TWOCAPTCHA

    url_request: str = f"http://api.{enums.ServiceEnm.TWOCAPTCHA.value}.com/2captcha/in.php"
    url_response: str = f"http://api.{enums.ServiceEnm.TWOCAPTCHA.value}.com/2captcha/res.php"

    def urls_set(self):
        """
        Set request/response URLs if they not set previously
        """
        if self.service_type == enums.ServiceEnm.DEATHBYCAPTCHA:
            self.url_request = f"http://api.{self.service_type}.com/2captcha/in.php"
            self.url_response = f"http://api.{self.service_type}.com/2captcha/res.php"
        else:
            self.url_request = f"https://api.{self.service_type}.com/createTask"
            self.url_response = f"https://api.{self.service_type}.com/getTaskResult"


"""
HTTP API Response
"""


class GetTaskResultResponseSer(MyBaseModel):
    status: str = "ready"
    solution: dict[str, str] | None = None
    cost: float = 0.0
    ip: str | None = None
    createTime: int | None = None
    endTime: int | None = None
    solveCount: int | None = None
    taskId: int | None = None
    # control method params
    balance: float | None = None
    # error info
    errorId: int = 0
    errorCode: str | None = None
    errorDescription: str | None = None
