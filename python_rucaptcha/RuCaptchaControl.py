import requests
import time

from .errors import RuCaptchaError
from .config import url_response


class RuCaptchaControl:
    def __init__(self, rucaptcha_key):
        self.RUCAPTCHA_KEY = rucaptcha_key

    def get_balance(self):
        '''
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        '''
        payload = {'key': self.RUCAPTCHA_KEY,
                   'action': 'getbalance',
                   'json': 1,
                   }
        # отправляем запрос на кол-во средств на аккаунте
        answer = requests.post(url_response, data = payload)

        if answer.json()['request'] == 'CAPCHA_NOT_READY':
            time.sleep(5)
        elif answer.json()["status"] == 0:
            return RuCaptchaError(answer.json()["request"])
        elif answer.json()["status"] == 1:
            return answer.json()['request']

    def complaint_on_result(self, reported_id):
        '''
        Позволяет отправить жалобуна неправильно решённую капчу.
        :param reported_id: Отправляете ID капчи на которую нужно пожаловаться
        :return: Возвращает результат действия
        '''
        payload = {'key': self.RUCAPTCHA_KEY,
                   'action': 'reportbad',
                   'id': reported_id,
                   'json': 1,
                   }
        # отправляем запрос на репорт
        answer = requests.post(url_response, data = payload)

        if answer.json()['request'] == 'CAPCHA_NOT_READY':
            time.sleep(5)
        elif answer.json()["status"] == 0:
            return RuCaptchaError(answer.json()["request"])
        elif answer.json()["status"] == 1:
            return answer.json()['request']

