import requests

from .errors import RuCaptchaError
from .config import url_response


class RuCaptchaControl:
    def __init__(self, rucaptcha_key):
        """
        Модуль отвечает за дополнительные действия с аккаунтом и капчей.
        :param rucaptcha_key: Ключ от RuCaptcha
        """
        self.payload = {'key': rucaptcha_key,
                        'json': 1,
                        }
        # результат возвращаемый методом *additional_methods*
        # в serverAnswer - ответ сервера на ваши действия,
        # в errorId - 0 - если всё хорошо, 1 - если есть ошибка,
        # в errorBody - тело ошибки, если есть
        self.result = {"serverAnswer": None,
                       "errorId": None,
                       "errorBody": None}

    def additional_methods(self, action, **kwargs):
        """
        Метод который выполняет дополнительные действия, такие как жалобы/получение баланса и прочее.
        :param action: Тип действия, самые типичные: getbalance(получение баланса),
                                                     reportbad(жалоба на неверное решение).
        :param kwargs: В качестве параметра можно передавать всё, что предусмотрено документацией.
        :return: Возвращает JSON строку с соответствующими полями:
                    {
                        "serverAnswer": string, ответ на ваши действия,
                        "errorId": int, 1(если ошибка) or 0(если действие выполнено),
                        "errorBody": string(тело ошибки, если произошла)
                    }
        Больше подробностей и примеров можно прочитать в 'CaptchaTester/rucaptcha_control_example.py'
        """

        # Если переданы ещё параметры - вносим их в payload
        if kwargs:
            for key in kwargs:
                self.payload.update({key: kwargs[key]})

        self.payload.update({'action': action})

        try:
            # отправляем на сервер данные с вашим запросом
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
