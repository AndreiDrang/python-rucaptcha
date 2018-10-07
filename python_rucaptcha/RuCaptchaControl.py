import aiohttp
import requests

from .errors import RuCaptchaError
from .config import url_request_2captcha, url_response_2captcha, url_request_rucaptcha, url_response_rucaptcha, \
    JSON_RESPONSE


class RuCaptchaControl:
    def __init__(self, rucaptcha_key: str, service_type: str='2captcha'):
        """
        Модуль отвечает за дополнительные действия с аккаунтом и капчей.
        :param rucaptcha_key: Ключ от RuCaptcha
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        """
        self.post_payload = {'key': rucaptcha_key,
                        'json': 1,
                             }

        # выбираем URL на который будут отпраляться запросы и с которого будут приходить ответы
        if service_type == '2captcha':
            self.url_request = url_request_2captcha
            self.url_response = url_response_2captcha
        elif service_type == 'rucaptcha':
            self.url_request = url_request_rucaptcha
            self.url_response = url_response_rucaptcha
        else:
            raise ValueError('Передан неверный параметр URL-сервиса капчи! Возможные варинты: `rucaptcha` и `2captcha`.'
                             'Wrong `service_type` parameter. Valid formats: `rucaptcha` or `2captcha`.')

    def additional_methods(self, action: str, **kwargs):
        """
        Метод который выполняет дополнительные действия, такие как жалобы/получение баланса и прочее.
        :param action: Тип действия, самые типичные: getbalance(получение баланса),
                                                     reportbad(жалоба на неверное решение).
        :param kwargs: В качестве параметра можно передавать всё, что предусмотрено документацией.
        :return: Возвращает JSON строку с соответствующими полями:
                    serverAnswer - ответ сервера при использовании RuCaptchaControl(баланс/жалобы и т.д.),
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - полная информация об ошибке:
                        {
                            text - Развернётое пояснение ошибки
                            id - уникальный номер ошибка в ЭТОЙ бибилотеке
                        }
        Больше подробностей и примеров можно прочитать в 'CaptchaTester/rucaptcha_control_example.py'
        """
        # результат возвращаемый методом *additional_methods*
        self.result = JSON_RESPONSE.copy()

        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        self.post_payload.update({'action': action})

        try:
            # отправляем на сервер данные с вашим запросом
            answer = requests.post(self.url_response, data = self.post_payload)
        except Exception as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                }
                                }
                               )
            return self.result

        if answer.json()["status"] == 0:
            self.result.update({'error': True,
                                'errorBody': RuCaptchaError().errors(answer.json()["request"])
                                }
                               )
            return self.result

        elif answer.json()["status"] == 1:
            self.result.update({
                                'serverAnswer': answer.json()['request']
                                }
                               )
            return self.result


# асинхронный метод
class aioRuCaptchaControl:
    def __init__(self, rucaptcha_key: str, service_type: str='2captcha'):
        """
        Асинхронный модуль отвечает за дополнительные действия с аккаунтом и капчей.
        :param rucaptcha_key: Ключ от RuCaptcha
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        """
        self.post_payload = {'key': rucaptcha_key,
                             'json': 1,
                             }

        # выбираем URL на который будут отпраляться запросы и с которого будут приходить ответы
        if service_type == '2captcha':
            self.url_request = url_request_2captcha
            self.url_response = url_response_2captcha
        elif service_type == 'rucaptcha':
            self.url_request = url_request_rucaptcha
            self.url_response = url_response_rucaptcha
        else:
            raise ValueError('Передан неверный параметр URL-сервиса капчи! Возможные варинты: `rucaptcha` и `2captcha`.'
                             'Wrong `service_type` parameter. Valid formats: `rucaptcha` or `2captcha`.')

    async def additional_methods(self, action: str, **kwargs):
        """
        Асинхронный метод который выполняет дополнительные действия, такие как жалобы/получение баланса и прочее.
        :param action: Тип действия, самые типичные: getbalance(получение баланса),
                                                     reportbad(жалоба на неверное решение).
        :param kwargs: В качестве параметра можно передавать всё, что предусмотрено документацией.
        :return: Возвращает JSON строку с соответствующими полями:
                    serverAnswer - ответ сервера при использовании RuCaptchaControl(баланс/жалобы и т.д.),
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - полная информация об ошибке:
                        {
                            text - Развернётое пояснение ошибки
                            id - уникальный номер ошибка в ЭТОЙ бибилотеке
                        }
        Больше подробностей и примеров можно прочитать в 'CaptchaTester/rucaptcha_control_example.py'
        """
        # результат возвращаемый методом *additional_methods*
        self.result = JSON_RESPONSE.copy()

        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        self.post_payload.update({'action': action})

        try:
            async with aiohttp.ClientSession() as session:
                # отправляем на сервер данные с вашим запросом
                async with session.post(self.url_response, data = self.post_payload) as resp:
                    answer = await resp.json()

        except Exception as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                }
                                }
                               )
            return self.result

        if answer["status"] == 0:
            self.result.update({'error': True,
                                'errorBody': RuCaptchaError().errors(answer["request"])
                                }
                               )
            return self.result

        elif answer["status"] == 1:
            self.result.update({
                                'serverAnswer': answer['request']
                                }
                               )
            return self.result