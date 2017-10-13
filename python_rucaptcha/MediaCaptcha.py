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
    def __init__(self, rucaptcha_key, recaptchavoice=False, solveaudio=False, sleep_time=5):
        """
        Метод создаёт папки, принимает параметры для работы c различными типами капчи.
        :param rucaptcha_key: Ключ от сайта RuCaptcha
        :param recaptchavoice: Передать True, если передаваемая капча является ReCaptcha
        :param solveaudio: Передать True, если передаваемая капча является SolveMedia
        :param sleep_time: Время ожидания решения капчи
        """
        self.recaptchavoice = recaptchavoice
        self.solveaudio = solveaudio

        self.RUCAPTCHA_KEY = rucaptcha_key
        self.sleep_time = sleep_time
        self.audio_path = os.path.normpath('mediacaptcha_audio')
        try:
            if not os.path.exists(self.audio_path):
                os.mkdir(self.audio_path)
            if not os.path.exists(".cache"):
                os.mkdir(".cache")
        except Exception as err:
            print(err)

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
            # Создаём пайлоад, вводим ключ от сайта, выбираем метод ПОСТ и ждём ответа в JSON-формате
            payload = {"key": self.RUCAPTCHA_KEY,
                       "method": "post",
                       "json": 1,
                       "soft_id": app_key}

            # В зависимости от переданного параметра выбирается тип капчи
            if self.recaptchavoice:
                payload.update({'recaptchavoice':1})
            elif self.solveaudio:
                payload.update({'solveaudio': 1})

            # Отправляем на рукапча аудио капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            captcha_id = requests.request('POST',
                                           url_request,
                                           data=payload,
                                           files=files).json()
        # Фильтрация ошибки
        if captcha_id['status'] is 0:
            return RuCaptchaError(captcha_id['request'])

        captcha_id = captcha_id['request']

        # удаляем файл капчи и врменные файлы
        os.remove(os.path.join(self.audio_path, 'aud-{0}.mp3'.format(audio_hash)))
        # Ожидаем решения капчи
        time.sleep(self.sleep_time)
        while True:
            # отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
            # если всё ок - идём дальше
            payload = {'key': self.RUCAPTCHA_KEY,
                       'action': 'get',
                       'id': captcha_id,
                       'json': 1,}
            # отправляем запрос на результат решения капчи, если не решена ожидаем
            captcha_response = requests.post(url_response, data = payload)
            if captcha_response.json()['request']=='CAPCHA_NOT_READY':
                time.sleep(self.sleep_time)
            elif captcha_response.json()["status"]==0:
                return RuCaptchaError(captcha_response.json()["request"])
            elif captcha_response.json()["status"]==1 :
                return captcha_response.json()['request']

    def __del__(self):
        if os.path.exists(".cache"):
            shutil.rmtree(".cache")
