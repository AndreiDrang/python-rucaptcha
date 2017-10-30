import requests
import os, shutil
import time
import hashlib

from .config import url_request, url_response, app_key
from .errors import RuCaptchaError


class MediaCaptcha:
    """
    Класс MediaCaptcha используется для решения аудиокапчи из ReCaptcha v2 и SolveMediaCaptcha
    """
    def __init__(self, rucaptcha_key, recaptchavoice=False, solveaudio=False, sleep_time=5, **kwargs):
        """
        Метод создаёт папки, принимает параметры для работы c различными типами капчи.
        :param rucaptcha_key: Ключ от сайта RuCaptcha
        :param recaptchavoice: Передать True, если передаваемая капча является ReCaptcha
        :param solveaudio: Передать True, если передаваемая капча является SolveMedia
        :param sleep_time: Время ожидания решения капчи
        """

        self.sleep_time = sleep_time
        self.audio_path = os.path.normpath('mediacaptcha_audio')
        try:
            if not os.path.exists(self.audio_path):
                os.mkdir(self.audio_path)
            if not os.path.exists(".cache"):
                os.mkdir(".cache")
        except Exception as err:
            print(err)
            
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
        
        # Если переданы ещё параметры - вносим их в payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': rucaptcha_key,
                            'action': 'get',
                            'json': 1,
                            }
        # результат возвращаемый методом *captcha_handler*
        # в captchaSolve - решение капчи,
        # в taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
        # в errorId - 0 - если всё хорошо, 1 - если есть ошибка,
        # в errorBody - тело ошибки, если есть.
        self.result = {"captchaSolve": None,
                       "taskId": None,
                       "errorId": None,
                       "errorBody": None}

    # Работа с капчёй
    def captcha_handler(self, audio_name=None, audio_download_link=None):
        """
        Метод полчает параметры и аозвращает решение капчи.
        Передаётся лишь один из параметров, либо audio_name либо audio_download_link.
        :param audio_name: Передаётся имя файла который должен лежать в папке с названием "mediacaptcha_audio", рядом со
                            скриптом.
        :param audio_download_link: Передаётся ссылка для скачивания аудио файла. Не ссылка на капчу или ещё что-либо.
                                    А именно ссылка по которой можно скачать аудио файл. Для последующей отправке RuCaptcha.
        :return: ВОзвращает решение капчи.
        """
        # Если передано имя файла - ищем его в папке, перименовываем
        if audio_name:
            audio_hash = hashlib.sha224(audio_name.encode('utf-8')).hexdigest()
            with open(os.path.join(self.audio_path, audio_name), 'rb') as audio_src:
                with open(os.path.join(self.audio_path, 'aud-{0}.mp3'.format(audio_hash)), 'wb') as audio_hash_src:
                    audio_hash_src.write(audio_src.read())

        # Если передана ссылка - скачиваем файл в папку, переименовываем и сохраняем
        elif audio_download_link:
            audio_hash = hashlib.sha224(audio_download_link.encode('utf-8')).hexdigest()
            content = requests.get(audio_download_link).content

            with open(os.path.join(self.audio_path,'aud-{0}.mp3'.format(audio_hash)), 'wb') as out:
                out.write(content)

        with open(os.path.join(self.audio_path, 'aud-{0}.mp3'.format(audio_hash)), 'rb') as captcha_audio:
            # Отправляем аудио файлом
            files = {'file': captcha_audio}

            # Отправляем на рукапча аудио капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            captcha_id = requests.request('POST',
                                           url_request,
                                           data=self.post_payload,
                                           files=files).json()
        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id['status'] is 0:
            self.result.update({'errorId': 1,
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
        os.remove(os.path.join(self.audio_path, 'aud-{0}.mp3'.format(audio_hash)))
        # Ожидаем решения капчи
        time.sleep(self.sleep_time)
        while True:
            # отправляем запрос на результат решения капчи, если не решена ожидаем
            captcha_response = requests.post(url_response, data = self.get_payload)

            # если капча ещё не решена - ожидаем
            if captcha_response.json()['request'] == 'CAPCHA_NOT_READY':
                time.sleep(self.sleep_time)

            # при ошибке во время решения
            elif captcha_response.json()["status"] == 0:
                self.result.update({'errorId': 1,
                                    'errorBody': RuCaptchaError().errors(captcha_response.json()["request"])
                                    }
                                   )
                return self.result

            # при решении капчи
            elif captcha_response.json()["status"] == 1:
                self.result.update({'errorId': 0,
                                    'captchaSolve': captcha_response.json()['request']
                                    }
                                   )
                return self.result
