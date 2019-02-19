import aiohttp
import requests

from python_rucaptcha.errors import RuCaptchaError
from python_rucaptcha.decorators import api_key_check, service_check


class RuCaptchaControl:
    def __init__(self, rucaptcha_key: str, service_type: str='2captcha', **kwargs):
        """
        Модуль отвечает за дополнительные действия с аккаунтом и капчей.
        :param rucaptcha_key: Ключ от RuCaptcha
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        """
        self.post_payload = {'key': rucaptcha_key,
                             'json': 1,
                            }
        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True
                      
    @api_key_check
    @service_check  
    def additional_methods(self, action: str):
        """
        Метод который выполняет дополнительные действия, такие как жалобы/получение баланса и прочее.
        :param action: Тип действия, самые типичные: getbalance(получение баланса),
                                                     reportbad(жалоба на неверное решение).
                                                     reportgood(оповещение при верном решении капчи, для сбора статистики по ReCaptcha V3)
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
        # result, url_response - задаются в декораторе `service_check`, после проверки переданного названия

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
    def __init__(self, rucaptcha_key: str, service_type: str='2captcha', **kwargs):
        """
        Асинхронный модуль отвечает за дополнительные действия с аккаунтом и капчей.
        :param rucaptcha_key: Ключ от RuCaptcha
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        """
        self.post_payload = {'key': rucaptcha_key,
                             'json': 1,
                             }

        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    @api_key_check
    @service_check
    async def additional_methods(self, action: str):
        """
        Асинхронный метод который выполняет дополнительные действия, такие как жалобы/получение баланса и прочее.
        :param action: Тип действия, самые типичные: getbalance(получение баланса),
                                                     reportbad(жалоба на неверное решение).
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
        # result, url_response - задаются в декораторе `service_check`, после проверки переданного названия

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
