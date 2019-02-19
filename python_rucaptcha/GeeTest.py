import requests
import time
import asyncio
import aiohttp

from python_rucaptcha.config import app_key
from python_rucaptcha.errors import RuCaptchaError
from python_rucaptcha.result_handler import get_sync_result, get_async_result
from python_rucaptcha.decorators import api_key_check, service_check


class GeeTest:
    def __init__(self, rucaptcha_key: str, gt: str, pageurl: str, service_type: str='2captcha', 
                api_server: str = None, sleep_time: int = 15, pingback: str = None, **kwargs):
        """
		Модуль отвечает за решение GeeTest
		:param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                                и "rucaptcha"
        :param gt: Публичный ключ сайта (статический)
        :param api_server: Домен API (обязателен для некоторых сайтов)
        :param pageurl: Полный URL страницы с капчей GeeTest
		:param sleep_time: Время ожидания решения
        :param pingback: URL для решения капчи с ответом через callback
        :param kwargs: Параметры для подключения к прокси.         
		"""
        # время ожидания решения капчи
        self.sleep_time = sleep_time
        # тип URL на с которым будет работать библиотека
        self.service_type = service_type

        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             'method': 'geetest',
                             "json": 1,
                             'gt': gt,
                             'pageurl': pageurl,
                             "soft_id": app_key}
        # добавляем api_server ксли передан
        if api_server:
            self.post_payload.update({'api_server': api_server})
        # если был передан параметр для callback`a - добавляем его
        if pingback:
            self.post_payload.update({'pingback': pingback})
        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': rucaptcha_key,
                            'action': 'get',
                            'json': 1,
                            }
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True		

    @api_key_check
    @service_check
    def captcha_handler(self, challenge: str, **kwargs):
        '''
		Метод отвечает за передачу данных на сервер для решения капчи
		:param challenge: Днамический ключ задания
		:param kwargs: Для передачи дополнительных параметров

		:return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - полная информация об ошибке:
                        {
                            text - Развернётое пояснение ошибки
                            id - уникальный номер ошибка в ЭТОЙ бибилотеке
                        }
		'''
        # result, url_request, url_response - задаются в декораторе `service_check`, после проверки переданного названия
        
        # Если переданы ещё параметры - вносим их в get_payload
        if kwargs:
            for key in kwargs:
                self.get_payload.update({key: kwargs[key]})

        # добавляем в пайлоад параметры капчи переданные пользователем
        self.post_payload.update({'challenge': challenge})
        # получаем ID капчи
        captcha_id = requests.post(self.url_request, data=self.post_payload).json()

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id['status'] == 0:
            self.result.update({'error': True,
                                'errorBody': RuCaptchaError().errors(captcha_id['request'])
                                }
                               )
            return self.result
        # иначе берём ключ отправленной на решение капчи и ждём решения
        else:
            captcha_id = captcha_id['request']
            # вписываем в taskId ключ отправленной на решение капчи
            self.result.update({"taskId": captcha_id})
            # обновляем пайлоад, вносим в него ключ отправленной на решение капчи
            self.get_payload.update({'id': captcha_id})

            # если передан параметр `pingback` - не ждём решения капчи а возвращаем незаполненный ответ
            if self.post_payload.get('pingback'):
                return self.get_payload
            
            else:
                # Ожидаем решения капчи
                time.sleep(self.sleep_time)
                return get_sync_result(get_payload=self.get_payload,
                                       sleep_time = self.sleep_time,
                                       url_response = self.url_response,
                                       result = self.result)
class aioGeeTest:
    def __init__(self, rucaptcha_key: str, gt: str, pageurl: str, service_type: str='2captcha', 
                api_server: str = None, sleep_time: int = 15, pingback: str = None, **kwargs):
        """
		Модуль отвечает за решение GeeTest
		:param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                                и "rucaptcha"
        :param gt: Публичный ключ сайта (статический)
        :param api_server: Домен API (обязателен для некоторых сайтов)
        :param pageurl: Полный URL страницы с капчей GeeTest
		:param sleep_time: Время ожидания решения
        :param pingback: URL для решения капчи с ответом через callback
		:param kwargs: Для передачи дополнительных параметров
		"""
        # время ожидания решения капчи
        self.sleep_time = sleep_time
        # тип URL на с которым будет работать библиотека
        self.service_type = service_type

        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             'method': 'geetest',
                             "json": 1,
                             'gt': gt,
                             'pageurl': pageurl,
                             "soft_id": app_key}
        # добавляем api_server ксли передан
        if api_server:
            self.post_payload.update({'api_server': api_server})
        # если был передан параметр для callback`a - добавляем его
        if pingback:
            self.post_payload.update({'pingback': pingback})
        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': rucaptcha_key,
                            'action': 'get',
                            'json': 1,
                            }
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True		

    @api_key_check
    @service_check
    async def captcha_handler(self, challenge: str, **kwargs):
        '''
		Метод отвечает за передачу данных на сервер для решения капчи
		:param challenge: Днамический ключ задания
		:param kwargs: Для передачи дополнительных параметров

		:return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - полная информация об ошибке:
                        {
                            text - Развернётое пояснение ошибки
                            id - уникальный номер ошибка в ЭТОЙ бибилотеке
                        }
		'''
        # result, url_request, url_response - задаются в декораторе `service_check`, после проверки переданного названия
        
        # Если переданы ещё параметры - вносим их в get_payload
        if kwargs:
            for key in kwargs:
                self.get_payload.update({key: kwargs[key]})

        # получаем ID капчи
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url_request, data=self.post_payload) as resp:
                captcha_id = await resp.json()

        # получаем ID капчи
        captcha_id = requests.post(self.url_request, data=self.post_payload).json()

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id['status'] == 0:
            self.result.update({'error': True,
                                'errorBody': RuCaptchaError().errors(captcha_id['request'])
                                }
                               )
            return self.result
        # иначе берём ключ отправленной на решение капчи и ждём решения
        else:
            captcha_id = captcha_id['request']
            # вписываем в taskId ключ отправленной на решение капчи
            self.result.update({"taskId": captcha_id})
            # обновляем пайлоад, вносим в него ключ отправленной на решение капчи
            self.get_payload.update({'id': captcha_id})

            # если передан параметр `pingback` - не ждём решения капчи а возвращаем незаполненный ответ
            if self.post_payload.get('pingback'):
                return self.get_payload
            
            else:
                # Ожидаем решения капчи
                await asyncio.sleep(self.sleep_time)
                return await get_async_result(get_payload = self.get_payload,
                                              sleep_time = self.sleep_time,
                                              url_response = self.url_response,
                                              result = self.result)
