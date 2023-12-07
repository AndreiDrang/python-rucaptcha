from typing import Literal, Optional

from msgspec import Struct

from . import enums
from .config import APP_KEY


class MyBaseModel(Struct):
    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}


"""
HTTP API Serializers
"""


class TaskSer(MyBaseModel):
    type: str


class ErrorFieldsSer(Struct):
    errorCode: str = None
    errorDescription: str = None


class CreateTaskBaseSer(MyBaseModel):
    clientKey: str
    task: TaskSer = {}
    languagePool: str = "en"
    callbackUrl: str = None
    soft_id: Literal[APP_KEY] = APP_KEY


class GetTaskResultRequestSer(MyBaseModel):
    clientKey: str
    taskId: int = None


class CaptchaOptionsSer(MyBaseModel):
    sleep_time: int = 10
    service_type: enums.ServiceEnm = enums.ServiceEnm.TWOCAPTCHA.value

    url_request: Optional[str] = None
    url_response: Optional[str] = None

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


class GetTaskResultResponseSer(MyBaseModel, ErrorFieldsSer):
    errorId: int = 0
    status: str = "ready"
    solution: dict = None
    cost: float = None
    ip: str = None
    createTime: int = None
    endTime: int = None
    solveCount: int = None
    taskId: int = None
    # control method params
    balance: float = None
