import requests
import time
import aiohttp
import asyncio

from requests.adapters import HTTPAdapter

from .config import url_request_2captcha, url_response_2captcha, url_request_rucaptcha, url_response_rucaptcha, app_key, \
    JSON_RESPONSE
from .errors import RuCaptchaError
from .result_handler import get_async_result, get_sync_result


class KeyCaptcha:
    '''
    Класс служит для решения KeyCaptcha
    '''

    def __init__(self, rucaptcha_key: str, service_type: str='2captcha', sleep_time: int=15):
        '''

        :param rucaptcha_key: АПИ ключ капчи из кабинета пользователя
        :param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        :param sleep_time: Время ожидания решения капчи
        '''
        self.RUCAPTCHA_KEY = rucaptcha_key
        if sleep_time < 15:
            raise ValueError(f'Параметр `sleep_time` должен быть не менее 5. Вы передали - {sleep_time}')
        self.sleep_time = sleep_time
        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': self.RUCAPTCHA_KEY,
                            'action': 'get',
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

        # создаём сессию
        self.session = requests.Session()
        # выставляем кол-во попыток подключения к серверу при ошибке
        self.session.mount('http://', HTTPAdapter(max_retries=5))

    def captcha_handler(self, **kwargs):
        # результат возвращаемый методом *captcha_handler*
        self.result = JSON_RESPONSE.copy()
        # считываем все переданные параметры KeyCaptcha
        try:
            self.s_s_c_user_id = kwargs['s_s_c_user_id']
            self.s_s_c_session_id = kwargs['s_s_c_session_id']
            self.s_s_c_web_server_sign = kwargs['s_s_c_web_server_sign']
            self.s_s_c_web_server_sign2 = kwargs['s_s_c_web_server_sign2']
            self.page_url = kwargs['page_url']
        except KeyError as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )
            return self.result

        # передаём параметры кей капчи для решения
        captcha_id = self.session.post(url=self.url_request, json={'key': self.RUCAPTCHA_KEY,
                                                                   's_s_c_user_id': self.s_s_c_user_id,
                                                                   's_s_c_session_id': self.s_s_c_session_id,
                                                                   's_s_c_web_server_sign': self.s_s_c_web_server_sign,
                                                                   's_s_c_web_server_sign2': self.s_s_c_web_server_sign2,
                                                                   'method': 'keycaptcha',
                                                                   'pageurl': self.page_url,
                                                                   'json': 1,
                                                                   'soft_id': app_key}).json()

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id['status'] is 0:
            self.result.update({'error': True,
                                'errorBody': RuCaptchaError().errors(captcha_id['request'])
                                }
                               )
            return self.result

        # иначе берём ключ отправленной на решение капчи и ждём решения
        else:
            captcha_id = captcha_id['request']

            # отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
            # если всё ок - идём дальше
            # вписываем в taskId ключ отправленной на решение капчи
            self.result.update({"taskId": captcha_id})
            # обновляем пайлоад, вносим в него ключ отправленной на решение капчи
            self.get_payload.update({'id': captcha_id})

            # Ожидаем решения капчи
            time.sleep(self.sleep_time)
            return get_async_result(get_payload = self.get_payload,
                                    sleep_time = self.sleep_time,
                                    url_response = self.url_response,
                                    result = self.result)

# асинхронный метод для решения FunCaptcha
class aioKeyCaptcha:
    '''
    Класс служит для решения KeyCaptcha
    '''

    def __init__(self, rucaptcha_key: str, service_type: str='2captcha', sleep_time: int=15, **kwargs):
        '''
        :param rucaptcha_key: АПИ ключ капчи из кабинета пользователя
        :param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        :param sleep_time: Время ожидания решения капчи
        '''
        self.RUCAPTCHA_KEY = rucaptcha_key
        if sleep_time < 15:
            raise ValueError(f'Параметр `sleep_time` должен быть не менее 5. Вы передали - {sleep_time}')
        self.sleep_time = sleep_time
        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': self.RUCAPTCHA_KEY,
                            'action': 'get',
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

        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             'method': 'keycaptcha',
                             "json": 1,
                             "soft_id": app_key}
        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': rucaptcha_key,
                            'action': 'get',
                            'json': 1,
                            }

    # Работа с капчей
    async def captcha_handler(self, **kwargs):
        # результат возвращаемый методом *captcha_handler*
        self.result = JSON_RESPONSE.copy()
        # считываем все переданные параметры KeyCaptcha
        try:
            self.s_s_c_user_id = kwargs['s_s_c_user_id']
            self.s_s_c_session_id = kwargs['s_s_c_session_id']
            self.s_s_c_web_server_sign = kwargs['s_s_c_web_server_sign']
            self.s_s_c_web_server_sign2 = kwargs['s_s_c_web_server_sign2']
            self.page_url = kwargs['page_url']
        except KeyError as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )
            return self.result
        try:
            # получаем ID капчи
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self.url_request, data={'key': self.RUCAPTCHA_KEY,
                                                                    's_s_c_user_id': self.s_s_c_user_id,
                                                                    's_s_c_session_id': self.s_s_c_session_id,
                                                                    's_s_c_web_server_sign': self.s_s_c_web_server_sign,
                                                                    's_s_c_web_server_sign2': self.s_s_c_web_server_sign2,
                                                                    'method': 'keycaptcha',
                                                                    'pageurl': self.page_url,
                                                                    'json': 1,
                                                                    'soft_id': app_key}) as resp:

                    captcha_id = await resp.json()

        except Exception as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )
            return self.result

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id['status'] is 0:
            self.result.update({'error': True,
                                'errorBody': RuCaptchaError().errors(captcha_id['request'])
                                }
                               )
            return self.result
        captcha_id = captcha_id['request']

        # отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
        # если всё ок - идём дальше
        # вписываем в taskId ключ отправленной на решение капчи
        self.result.update({"taskId": captcha_id})
        # обновляем пайлоад, вносим в него ключ отправленной на решение капчи
        self.get_payload.update({'id': captcha_id})

        # Ожидаем решения капчи
        await asyncio.sleep(self.sleep_time)
        # отправляем запрос на результат решения капчи, если не решена ожидаем
        return await get_async_result(get_payload = self.get_payload,
                                      sleep_time = self.sleep_time,
                                      url_response = self.url_response,
                                      result = self.result)
