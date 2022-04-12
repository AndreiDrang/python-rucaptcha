import requests
from requests.adapters import HTTPAdapter

from . import enums
from .serializer import ResponseSer, GetRequestSer, PostRequestSer, CaptchaOptionsSer


class BaseCaptcha:
    def __init__(
        self, rucaptcha_key: str, sleep_time: int = 15, service_type: str = enums.ServicesEnm.TWOCAPTCHA.value, **kwargs
    ):
        """
        :param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
        :param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        :param kwargs: Служит для передачи необязательных параметров в пайлоад для запроса к RuCaptcha
        """
        # assign args to validator
        self.params = CaptchaOptionsSer(**locals())

        # prepare POST payload
        self.post_payload = PostRequestSer(key=self.params.rucaptcha_key, method="geetest").dict(by_alias=True)
        # prepare GET payload
        self.get_payload = GetRequestSer(key=self.params.rucaptcha_key).dict(by_alias=True, exclude_none=True)
        # prepare result payload
        self.result = ResponseSer()

        # If more parameters are passed, add them to post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        # prepare session
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=5))
        self.session.mount("https://", HTTPAdapter(max_retries=5))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True
