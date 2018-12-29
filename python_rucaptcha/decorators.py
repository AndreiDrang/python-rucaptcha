from .errors import RuCaptchaError
from .config import url_request_2captcha, url_response_2captcha, url_request_rucaptcha, url_response_rucaptcha, JSON_RESPONSE


def api_key_check(func):
    """
    Декоратор проверяет переданный параметр `rucaptcha_key` на корректность
    """
    def wrapper(self, *args, **kwargs):
        # результат возвращаемый методом *captcha_handler*
        self.result = JSON_RESPONSE.copy()
        # проверяет длинну ключа API
        if len(self.post_payload.get('key'))==32:
            return func(self, *args, **kwargs)
        else:
            self.result.update({'error': True,
                                'errorBody': RuCaptchaError().errors('ERROR_WRONG_USER_KEY')
                                })
            return self.result
            
    return wrapper

def service_check(func):
    """
    Декоратор проверяет переданный параметр `service_type` на корректность
    и задаёт соответствующие URL'ы для работы
    """
    def wrapper(self, *args, **kwargs):
        # проверяем, находится для типа сервиса в списке
        if self.service_type in ('2captcha', 'rucaptcha'):
            # задаём URL в соответствии от типа сервиса
            if self.service_type == '2captcha':
                self.url_request = url_request_2captcha
                self.url_response = url_response_2captcha
            elif self.service_type == 'rucaptcha':
                self.url_request = url_request_rucaptcha
                self.url_response = url_response_rucaptcha
            return func(self, *args, **kwargs)
        # вызываем ошибку, если сервис неизвестный
        else:
            raise ValueError('Передан неверный параметр URL-сервиса капчи! Возможные варинты: `rucaptcha` и `2captcha`.'
                             'Wrong `service_type` parameter. Valid formats: `rucaptcha` or `2captcha`.')

    return wrapper
