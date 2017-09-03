import requests
import time
from errors import RuCaptchaError
from config import url_response


class RuCaptchaControl:
    def __init__(self, rucaptcha_key):
        self.RUCAPTCHA_KEY = rucaptcha_key

    def get_balance(self):
        '''
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        '''
        answer = requests.get(url_response+"?action=getbalance&json=1&key={0}".format(self.RUCAPTCHA_KEY))
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
        answer = requests.get(url_response + "?action=reportbad&json=1&id={0}&key={1}".format(reported_id,
                                                                                              self.RUCAPTCHA_KEY))

        if answer.json()['request'] == 'CAPCHA_NOT_READY':
            time.sleep(5)
        elif answer.json()["status"] == 0:
            return RuCaptchaError(answer.json()["request"])
        elif answer.json()["status"] == 1:
            return answer.json()['request']

