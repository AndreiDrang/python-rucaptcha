import requests
import time
import asyncio
import aiohttp

from python_rucaptcha.config import app_key
from python_rucaptcha.errors import RuCaptchaError
from python_rucaptcha.result_handler import get_sync_result, get_async_result
from python_rucaptcha.decorators import api_key_check, service_check


class TextCaptcha:

    def __init__(self, rucaptcha_key: str, sleep_time: int=5, service_type: str='2captcha', pingback: str=None, **kwargs):        
        """
		Инициализация нужных переменных.
		:param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
		:param sleep_time: Время ожидания решения капчи
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        :param pingback: Параметр для ссылки с на которой будет ожидание callback ответа от RuCaptcha
		:param kwargs: Для передачи дополнительных параметров
		"""
        # время ожидания решения капчи
        self.sleep_time = sleep_time
        # тип URL на с которым будет работать библиотека
        self.service_type = service_type
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             "method": "post",
                             "json": 1,
                             "soft_id": app_key,
                             }
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
    def captcha_handler(self, captcha_text: str, **kwargs):
        '''
		Метод отвечает за передачу данных на сервер для решения капчи
		:param captcha_text: Текстовый вопрос
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

        # вводим текст капчи, выбираем метод ПОСТ и ждём ответа. в JSON-формате
        self.post_payload.update({"textcaptcha": captcha_text})
        # Отправляем на рукапча текст капчи и ждём ответа
        #  в результате получаем JSON ответ с номером решаемой капчи
        captcha_id = requests.post(self.url_request,
                                       data=self.post_payload).json()

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
                return get_sync_result(get_payload = self.get_payload,
                                       sleep_time = self.sleep_time,
                                       url_response = self.url_response,
                                       result = self.result)


# асинхронный метод для решения текстовой капчи
class aioTextCaptcha:

    def __init__(self, rucaptcha_key: str, sleep_time: int=5, service_type: str='2captcha', pingback: str=None, **kwargs):
        """
		Инициализация нужных переменных.
		:param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
		:param sleep_time: Время ожидания решения капчи
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        :param pingback: Параметр для ссылки с на которой будет ожидание callback ответа от RuCaptcha
		:param kwargs: Для передачи дополнительных параметров
		"""
        # время ожидания решения капчи
        self.sleep_time = sleep_time
        # тип URL на с которым будет работать библиотека
        self.service_type = service_type
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             "method": "post",
                             "json": 1,
                             "soft_id": app_key,
                             }
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
    async def captcha_handler(self, captcha_text: str, **kwargs):
        '''
		Метод отвечает за передачу данных на сервер для решения капчи
		:param captcha_text: Текстовый вопрос
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
                
        # вводим текст капчи, выбираем метод ПОСТ и ждём ответа. в JSON-формате
        self.post_payload.update({"textcaptcha": captcha_text})
        # получаем ID капчи
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url_request, data = self.post_payload) as resp:
                captcha_id = await resp.json()

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
