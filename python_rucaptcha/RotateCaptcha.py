import requests
import time
import asyncio
import aiohttp
from requests.adapters import HTTPAdapter

from python_rucaptcha.config import app_key
from python_rucaptcha.errors import RuCaptchaError
from python_rucaptcha.result_handler import get_sync_result, get_async_result
from python_rucaptcha.decorators import api_key_check, service_check


class RotateCaptcha:
    def __init__(self, rucaptcha_key: str, service_type: str='2captcha', sleep_time: int=5, pingback: str = ''):
        '''
        Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удалются временные фалйы и папки
        :param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param service_type: Тип сервиса через который будет работать билиотека. Доступны `rucaptcha` или `2captcha`
        :param sleep_time: Вермя ожидания решения капчи
        '''
        # время ожидания решения капчи
        self.sleep_time = sleep_time
        # тип URL на с которым будет работать библиотека
        self.service_type = service_type
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             'method': 'rotatecaptcha',
                             "json": 1,
                             "soft_id": app_key}

        # если был передан параметр для callback`a - добавляем его
        if pingback:
            self.post_payload.update({'pingback': pingback})

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': rucaptcha_key,
                            'action': 'get',
                            'json': 1,
                            }

        # создаём сессию
        self.session = requests.Session()
        # выставляем кол-во попыток подключения к серверу при ошибке
        self.session.mount('http://', HTTPAdapter(max_retries = 5))
        self.session.mount('https://', HTTPAdapter(max_retries = 5))

    @api_key_check
    @service_check
    def captcha_handler(self, captcha_link: str):
        '''
        Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
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
       
        # Скачиваем изображение
        content = self.session.get(captcha_link).content

        # Отправляем изображение файлом
        files = {'file': content}
        # Отправляем на рукапча изображение капчи и другие парметры,
        # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
        captcha_id = self.session.post(self.url_request, data=self.post_payload, files=files).json()

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
            # вписываем в taskId ключ отправленной на решение капчи
            self.result.update({"taskId": captcha_id})
            # обновляем пайлоад, вносим в него ключ отправленной на решение капчи
            self.get_payload.update({'id': captcha_id})

            # если передан параметр `pingback` - не ждём решения капчи а возвращаем незаполненный ответ
            if self.post_payload.get('pingback'):
                return self.get_payload
            
            else:
                # Ожидаем решения капчи 20 секунд
                time.sleep(self.sleep_time)
                return get_sync_result(get_payload=self.get_payload,
                                       sleep_time = self.sleep_time,
                                       url_response = self.url_response,
                                       result = self.result)

