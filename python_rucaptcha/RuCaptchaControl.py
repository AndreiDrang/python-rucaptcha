import requests
from config import url_response


class RuCaptchaControl:
    def __init__(self, rucaptcha_key):
        self.RECAPTCHA_KEY = rucaptcha_key

    def get_balance(self):
        answer = requests.get(url_response+"?action=getbalance&json=1&key={0}".format(self.RECAPTCHA_KEY))
        return answer.json()

    def complaint_on_result(self, reported_id):
        answer = requests.get(url_response + "?action=reportbad&json=1&id={0}&key={1}".format(reported_id,
                                                                                              self.RECAPTCHA_KEY))
        if answer.json()["request"] == "OK_REPORT_RECORDED":
            return {'status': 'OK'}
        else:
            return {'status': 'Error', 'err': answer.json()["request"]}
