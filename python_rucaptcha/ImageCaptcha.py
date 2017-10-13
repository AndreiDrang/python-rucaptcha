import requests
import time
import tempfile
import hashlib
import os

from .config import url_request, url_response, app_key
from .errors import RuCaptchaError


class ImageCaptcha:
    '''
    Данный метод подходит как для загрузки и решения обычной капчи
    так и для большой капчи.
    Требуется передать API ключ сайта, ссылку на изображение и,по желанию, время ожидания решения капчи
    Подробней информацию смотрите в методе 'captcha_handler'
    '''

    def __init__(self, rucaptcha_key, sleep_time=5, save_format = 'temp'):
        '''
        Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удалются временные фалйы и папки
        :param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
        :param save_format: Формат в котором будет сохраняться изображение, либо как временный фпйл - 'temp',
                            либо как обычное изображение в папку созданную библиотекой - 'const'.
        '''
        self.RUCAPTCHA_KEY = rucaptcha_key
        self.sleep_time = sleep_time
        self.save_format = save_format

    def image_temp_saver(self, content):
        '''
        Метод сохраняет файл изображения как временный и отправляет его сразу на сервер для расшифровки.
        :return: Возвращает ID капчи
        '''
        with tempfile.NamedTemporaryFile(suffix='.png') as out:
            out.write(content)
            captcha_image = open(out.name, 'rb')
            # Отправляем изображение файлом
            files = {'file': captcha_image}
            # Создаём пайлоад, вводим ключ от сайта, выбираем метод ПОСТ и ждём ответа в JSON-формате
            payload = {"key": self.RUCAPTCHA_KEY,
                       "method": "post",
                       "json": 1,
                       "soft_id": app_key
                       }

            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            captcha_id = (requests.request('POST',
                                           url_request,
                                           data=payload,
                                           files=files).json())
        return captcha_id

    def image_const_saver(self, content):
        '''
        Метод создаёт папку и сохраняет в неё изображение, затем передаёт его на расшифровку и удалет файл.
        :return: Возвращает ID капчи
        '''
        img_path = 'PythonRuCaptchaImages'

        if not os.path.exists(img_path):
            os.mkdir(img_path)

        # Высчитываем хэш изображения, для того что бы сохранить его под уникальным именем
        image_hash = hashlib.sha224(content).hexdigest()

        with open(os.path.join(img_path, 'im-{0}.png'.format(image_hash)), 'wb') as out_image:
            out_image.write(content)

        with open(os.path.join(img_path, 'im-{0}.png'.format(image_hash)), 'rb') as captcha_image:
            # Отправляем изображение файлом
            files = {'file': captcha_image}
            # Создаём пайлоад, вводим ключ от сайта, выбираем метод ПОСТ и ждём ответа в JSON-формате
            payload = {"key": self.RUCAPTCHA_KEY,
                       "method": "post",
                       "json": 1,
                       "soft_id": app_key
                       }
            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            captcha_id = (requests.request('POST',
                                           url_request,
                                           data=payload,
                                           files=files).json())

        # удаляем файл капчи и врменные файлы
        os.remove(os.path.join(img_path, "im-{0}.png".format(image_hash)))

        return captcha_id

    # Работа с капчёй
    def captcha_handler(self, captcha_link):
        '''
        Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
        :return: Ответ на капчу
        '''

        content = requests.get(captcha_link).content

        # согласно значения переданного параметра выбираем функцию для сохранения изображения
        if self.save_format == 'const':
            captcha_id = self.image_const_saver(content)
        elif self.save_format == 'temp':
            captcha_id = self.image_temp_saver(content)
        else:
            return """Wrong 'save_format' parameter. Valid formats: 'const' or 'temp'.\n 
                    Неправильный 'save_format' параметр. Возможные форматы: 'const' или 'temp'."""

        if captcha_id['status'] is 0:
            return RuCaptchaError(captcha_id['request'])

        captcha_id = captcha_id['request']

        # Ожидаем решения капчи
        time.sleep(self.sleep_time)
        while True:
            # отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
            # если всё ок - идём дальше
            payload = {'key': self.RUCAPTCHA_KEY,
                       'action': 'get',
                       'id': captcha_id,
                       'json': 1,
                       }
            # отправляем запрос на результат решения капчи, если не решена ожидаем
            captcha_response = requests.post(url_response, data = payload)
            if captcha_response.json()['request'] == 'CAPCHA_NOT_READY':
                time.sleep(self.sleep_time)
            elif captcha_response.json()["status"] == 0:
                return RuCaptchaError(captcha_response.json()["request"])
            elif captcha_response.json()["status"] == 1:
                return captcha_response.json()['request']
