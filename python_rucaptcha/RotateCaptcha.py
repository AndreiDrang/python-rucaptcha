import requests
import time
import tempfile

from .config import url_request, url_response, app_key
from .errors import RuCaptchaError

class RotateCaptcha:
    def __init__(self, rucaptcha_key, sleep_time=5):
        '''
        Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удалются временные фалйы и папки
        :param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
        '''
        self.RUCAPTCHA_KEY = rucaptcha_key
        self.sleep_time = sleep_time

    # Работа с капчёй
    def captcha_handler(self, captcha_link):
        '''
        Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
        :return: Ответ на капчу
        '''
        # Скачиваем изображение
        content = requests.get(captcha_link).content
        with tempfile.NamedTemporaryFile(suffix='.jpg') as out:
            out.write(content)
            captcha_image = open(out.name, 'rb')
            # Отправляем изображение файлом
            files = {'file': captcha_image}
            # Создаём пайлоад, вводим ключ от сайта, выбираем метод ПОСТ и ждём ответа в JSON-формате
            payload = {"key": self.RUCAPTCHA_KEY,
                       "method": "rotatecaptcha",
                       "json": 1,
                       "soft_id":app_key}


            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            captcha_id = requests.request('POST',
                                            url_request,
                                            data=payload,
                                            files=files).json()

        if captcha_id['status'] is 0:
            return RuCaptchaError(captcha_id['request'])

        captcha_id = captcha_id['request']

        # Ожидаем решения капчи
        time.sleep(self.sleep_time)
        while True:
            # отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
            # если всё ок - идём дальше
            captcha_response = requests.request('GET',
                                                url_response+"?key={0}&action=get&id={1}&json=1"
                                                .format(self.RUCAPTCHA_KEY, captcha_id))
            if captcha_response.json()['request']=='CAPCHA_NOT_READY':
                time.sleep(self.sleep_time)
            elif captcha_response.json()["status"]==0:
                return RuCaptchaError(captcha_response.json()["request"])
            elif captcha_response.json()["status"]==1 :
                return captcha_response.json()['request']

