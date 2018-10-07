import requests
import os
import time
import hashlib
from requests.adapters import HTTPAdapter

from .config import url_request_2captcha, url_response_2captcha, url_request_rucaptcha, url_response_rucaptcha, app_key,\
    JSON_RESPONSE
from .errors import RuCaptchaError
from .result_handler import get_sync_result, get_async_result


class MediaCaptcha:
    """
    Класс MediaCaptcha используется для решения аудиокапчи из ReCaptcha v2 и SolveMediaCaptcha
    """
    def __init__(self, rucaptcha_key: str, service_type: str='2captcha', recaptchavoice: bool=False,
                 solveaudio: bool=False, sleep_time: int=5, **kwargs):
        """
        Метод создаёт папки, принимает параметры для работы c различными типами капчи.
        :param rucaptcha_key: Ключ от сайта RuCaptcha
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        :param recaptchavoice: Передать True, если передаваемая капча является ReCaptcha
        :param solveaudio: Передать True, если передаваемая капча является SolveMedia
        :param sleep_time: Время ожидания решения капчи
        """
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

        if sleep_time < 5:
            raise ValueError(f'Параметр `sleep_time` должен быть не менее 10. Вы передали - {sleep_time}')
        self.sleep_time = sleep_time

        self.audio_path = os.path.normpath('mediacaptcha_audio')

        if not os.path.exists(self.audio_path):
            os.mkdir(self.audio_path)
        if not os.path.exists(".cache"):
            os.mkdir(".cache")

        # Тело пост запроса при отправке капчи на решение
        self.post_payload = {"key": rucaptcha_key,
                             "method": "post",
                             "json": 1,
                             "soft_id": app_key,
                             }
        # В зависимости от переданного параметра выбирается тип капчи
        if recaptchavoice:
            self.post_payload.update({'recaptchavoice': 1})
        elif solveaudio:
            self.post_payload.update({'solveaudio': 1})
        
        # Если переданы ещё параметры - вносим их в post_payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': rucaptcha_key,
                            'action': 'get',
                            'json': 1,
                            }

        # создаём сессию
        self.session = requests.Session()
        # выставляем кол-во попыток подключения к серверу при ошибке
        self.session.mount('http://', HTTPAdapter(max_retries=5))

    # Работа с капчёй
    def captcha_handler(self, audio_name: str=None, audio_download_link: str=None):
        """
        Метод полчает параметры и аозвращает решение капчи.
        Передаётся лишь один из параметров, либо audio_name либо audio_download_link.
        :param audio_name: Передаётся имя файла который должен лежать в папке с названием "mediacaptcha_audio", рядом со
                            скриптом.
        :param audio_download_link: Передаётся ссылка для скачивания аудио файла. Не ссылка на капчу или ещё что-либо.
                                    А именно ссылка по которой можно скачать аудио файл. Для последующей отправке RuCaptcha.
        :return: Возвращает решение капчи.
        """
        # результат возвращаемый методом *captcha_handler*
        self.result = JSON_RESPONSE.copy()
        if audio_name or audio_download_link:
            # Если передано имя файла - ищем его в папке, перименовываем
            if audio_name:
                audio_hash = hashlib.sha224(audio_name.encode('utf-8')).hexdigest()
                with open(os.path.join(self.audio_path, audio_name), 'rb') as audio_src:
                    with open(os.path.join(self.audio_path, f'aud-{audio_hash}.mp3'), 'wb') as audio_hash_src:
                        audio_hash_src.write(audio_src.read())

            # Если передана ссылка - скачиваем файл в папку, переименовываем и сохраняем
            elif audio_download_link:
                audio_hash = hashlib.sha224(audio_download_link.encode('utf-8')).hexdigest()
                content = requests.get(audio_download_link).content

                with open(os.path.join(self.audio_path,f'aud-{audio_hash}.mp3'), 'wb') as out:
                    out.write(content)
        else:
            raise ValueError('Не передан ни один из параметров для открытия аудио(audio_name) или скачивания(audio_download_link)'
                             'One parameter is required: audio_name or audio_download_link')

        with open(os.path.join(self.audio_path, f'aud-{audio_hash}.mp3'), 'rb') as captcha_audio:
            # Отправляем аудио файлом
            files = {'file': captcha_audio}

            # Отправляем на рукапча аудио капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            captcha_id = requests.request('POST',
                                           self.url_request,
                                           data=self.post_payload,
                                           files=files).json()
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

        # удаляем файл капчи
        os.remove(os.path.join(self.audio_path, f'aud-{audio_hash}.mp3'))
        # Ожидаем решения капчи
        time.sleep(self.sleep_time)
        return get_sync_result(get_payload=self.get_payload,
                               sleep_time = self.sleep_time,
                               url_response = self.url_response,
                               result = self.result)
