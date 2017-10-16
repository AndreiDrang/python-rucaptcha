import requests

from .errors import RuCaptchaError
from .config import url_response


class RuCaptchaControl:
    def __init__(self, rucaptcha_key):
        self.payload = {'key': rucaptcha_key,
                        'json': 1,
                        }
        # результат возвращаемый методом *captcha_handler*
        # в serverAnswer - ответ сервера на ваши действия,
        # в errorId - 0 - если всё хорошо, 1 - если есть ошибка,
        # в errorBody - тело ошибки, если есть
        self.result = {"serverAnswer": None,
                       "errorId": None,
                       "errorBody": None}

    def additional_methods(self, action, **kwargs):

        # Если переданы ещё параметры - вносим их в payload
        if kwargs:
            for key in kwargs:
                self.payload.update({key: kwargs[key]})

        self.payload.update({'action': action})

        try:
            # отправляем запрос на сервер с вашим запросом
            answer = requests.post(url_response, data = self.payload)
        except Exception as error:
            self.result.update({'errorId': 1,
                                'errorBody': error,
                                }
                               )
            return self.result

        if answer.json()["status"] == 0:
            self.result.update({'errorId': 1,
                                'errorBody': RuCaptchaError().errors(answer.json()["request"])
                                }
                               )
            return self.result

        elif answer.json()["status"] == 1:
            self.result.update({'errorId': 0,
                                'serverAnswer': answer.json()['request']
                                }
                               )
            return self.result
