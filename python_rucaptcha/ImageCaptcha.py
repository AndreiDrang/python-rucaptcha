import requests
import time
import tempfile
import hashlib
import os
import asyncio
import aiohttp
import base64

from .config import url_request, url_response, app_key
from .errors import RuCaptchaError


class ImageCaptcha:
    """
    Данный метод подходит как для загрузки и решения обычной капчи
    так и для большой капчи.
    Требуется передать API ключ сайта, ссылку на изображение и,по желанию, время ожидания решения капчи
    Подробней информацию смотрите в методе 'captcha_handler'
    """

    def __init__(self, rucaptcha_key, sleep_time=5, save_format='temp', **kwargs):
        """
        Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удалются временные фалйы и папки
        :param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
        :param save_format: Формат в котором будет сохраняться изображение, либо как временный фпйл - 'temp',
                            либо как обычное изображение в папку созданную библиотекой - 'const'.
        :param kwargs: Служит для передачи необязательных параметров.

        Подробней с примерами можно ознакомиться в 'CaptchaTester/image_captcha_example.py'
        """
        self.RUCAPTCHA_KEY = rucaptcha_key
        self.sleep_time = sleep_time
        self.save_format = save_format
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": self.RUCAPTCHA_KEY,
                             "method": "base64",
                             "json": 1,
                             "soft_id": app_key,
                             }
        # Если переданы ещё параметры - вносим их в payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': self.RUCAPTCHA_KEY,
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

    def image_temp_saver(self, content):
        """
        Метод сохраняет файл изображения как временный и отправляет его сразу на сервер для расшифровки.
        :return: Возвращает ID капчи из сервиса
        """
        with tempfile.NamedTemporaryFile(suffix='.png') as out:
            out.write(content)
            captcha_image = open(out.name, 'rb')
            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            self.post_payload.update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
            captcha_id = (requests.post(url_request, data=self.post_payload).json())

        return captcha_id

    def image_const_saver(self, content):
        """
        Метод создаёт папку и сохраняет в неё изображение, затем передаёт его на расшифровку и удалет файл.
        :return: Возвращает ID капчи из сервиса
        """
        img_path = 'PythonRuCaptchaImages'

        if not os.path.exists(img_path):
            os.mkdir(img_path)

        # Высчитываем хэш изображения, для того что бы сохранить его под уникальным именем
        image_hash = hashlib.sha224(content).hexdigest()

        with open(os.path.join(img_path, 'im-{0}.png'.format(image_hash)), 'wb') as out_image:
            out_image.write(content)

        with open(os.path.join(img_path, 'im-{0}.png'.format(image_hash)), 'rb') as captcha_image:
            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            self.post_payload.update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
            captcha_id = (requests.post(url_request, data=self.post_payload).json())

        # удаляем файл капчи
        os.remove(os.path.join(img_path, "im-{0}.png".format(image_hash)))

        return captcha_id

    def local_image_captcha(self, content):
        """
        Метод получает в качестве параметра ссылку на локальный файл, считывает изображение и отправляет его на РуКапчу
        для проверки и получения её ID
        :param content: Ссылка на локальный файл
        :return: ID капчи в сервисе
        """
        try:
            with open(content, 'rb') as captcha_image:
                # Отправляем на рукапча изображение капчи и другие парметры,
                # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
                self.post_payload.update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
                captcha_id = (requests.post(url_request, data=self.post_payload).json())

        except IOError:
            return 'File not found!'

        return captcha_id

    # Работа с капчёй
    def captcha_handler(self, captcha_link=None, captcha_file=None):
        """
        Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
        :return: Ответ на капчу в виде JSON строки с полями:
                                                            captchaSolve - решение капчи,
                                                            taskId - находится Id задачи на решение капчи,
                                                            errorId - 0 - если всё хорошо, 1 - если есть ошибка,
                                                            errorBody - тело ошибки, если есть.
        """

        # если передана локальная ссылка н файл - работаем с ним
        if captcha_file:
            captcha_id = self.local_image_captcha(captcha_file)
        # если передан URL - используем его
        elif captcha_link:
            try:
                content = requests.get(captcha_link).content
            except Exception as error:
                self.result.update({'errorId': 1,
                                    'errorBody': error,
                                    }
                                   )
                return self.result

            # согласно значения переданного параметра выбираем функцию для сохранения изображения
            if self.save_format == 'const':
                captcha_id = self.image_const_saver(content)
            elif self.save_format == 'temp':
                captcha_id = self.image_temp_saver(content)
            else:
                return """Wrong 'save_format' parameter. Valid formats: 'const' or 'temp'.\n 
                        Неправильный 'save_format' параметр. Возможные форматы: 'const' или 'temp'."""
        else:
            return """You did not send any file local link or URL."""

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

        # Ожидаем решения капчи
        time.sleep(self.sleep_time)
        while True:
            # отправляем запрос на результат решения капчи, если не решена ожидаем
            captcha_response = requests.post(url_response, data=self.get_payload)

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


class aioImageCaptcha:
    """
    Данный асинхронный метод подходит как для загрузки и решения обычной капчи
    так и для большой капчи.
    Требуется передать API ключ сайта, ссылку на изображение и,по желанию, время ожидания решения капчи
    Подробней информацию смотрите в методе 'captcha_handler'
    """

    def __init__(self, rucaptcha_key, sleep_time=5, save_format='temp', **kwargs):
        """
        Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удалются временные фалйы и папки
        :param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
        :param save_format: Формат в котором будет сохраняться изображение, либо как временный фпйл - 'temp',
                            либо как обычное изображение в папку созданную библиотекой - 'const'.
        :param kwargs: Служит для передачи необязательных параметров.

        Подробней с примерами можно ознакомиться в 'CaptchaTester/image_captcha_example.py'
        """
        self.RUCAPTCHA_KEY = rucaptcha_key
        self.sleep_time = sleep_time
        self.save_format = save_format
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": self.RUCAPTCHA_KEY,
                             "method": "base64",
                             "json": 1,
                             "soft_id": app_key,
                             }
        # Если переданы ещё параметры - вносим их в payload
        if kwargs:
            for key in kwargs:
                self.post_payload.update({key: kwargs[key]})

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': self.RUCAPTCHA_KEY,
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

    async def image_temp_saver(self, content):
        """
        Метод сохраняет файл изображения как временный и отправляет его сразу на сервер для расшифровки.
        :return: Возвращает ID капчи из сервиса
        """
        with tempfile.NamedTemporaryFile(suffix='.png') as out:
            out.write(content)
            captcha_image = open(out.name, 'rb')
            # Отправляем изображение файлом
            self.post_payload.update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
            async with aiohttp.ClientSession() as session:
                async with session.post(url_request, data=self.post_payload) as resp:
                    captcha_id = await resp.json()

        return captcha_id

    async def image_const_saver(self, content):
        """
        Метод создаёт папку и сохраняет в неё изображение, затем передаёт его на расшифровку и удалет файл.
        :return: Возвращает ID капчи из сервиса
        """
        img_path = 'PythonRuCaptchaImages'

        if not os.path.exists(img_path):
            os.mkdir(img_path)

        # Высчитываем хэш изображения, для того что бы сохранить его под уникальным именем
        image_hash = hashlib.sha224(content).hexdigest()

        with open(os.path.join(img_path, 'im-{0}.png'.format(image_hash)), 'wb') as out_image:
            out_image.write(content)

        with open(os.path.join(img_path, 'im-{0}.png'.format(image_hash)), 'rb') as captcha_image:
            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            self.post_payload.update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
            async with aiohttp.ClientSession() as session:
                async with session.post(url_request, data=self.post_payload) as resp:
                    captcha_id = await resp.json()

        # удаляем файл капчи
        os.remove(os.path.join(img_path, "im-{0}.png".format(image_hash)))

        return captcha_id

    async def local_image_captcha(self, content):
        """
        Метод получает в качестве параметра ссылку на локальный файл, считывает изображение и отправляет его на РуКапчу
        для проверки и получения её ID
        :param content: Ссылка на локальный файл
        :return: ID капчи в сервисе
        """
        try:
            with open(content, 'rb') as captcha_image:
                # Отправляем на рукапча изображение капчи и другие парметры,
                # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
                self.post_payload.update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
                captcha_id = (requests.post(url_request, data=self.post_payload).json())

        except IOError:
            return 'File not found!'

        return captcha_id

    # Работа с капчёй
    async def captcha_handler(self, captcha_link=None, captcha_file=None):
        """
        Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
        :return: Ответ на капчу в виде JSON строки с полями:
                                                            captchaSolve - решение капчи,
                                                            taskId - находится Id задачи на решение капчи,
                                                            errorId - 0 - если всё хорошо, 1 - если есть ошибка,
                                                            errorBody - тело ошибки, если есть.
        """

        # если передана локальная ссылка н файл - работаем с ним
        if captcha_file:
            captcha_id = await self.local_image_captcha(captcha_file)

        elif captcha_link:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(captcha_link) as resp:
                        content = await resp.content.read()
            except Exception as error:
                self.result.update({'errorId': 1,
                                    'errorBody': error,
                                    }
                                   )
                return self.result

            # согласно значения переданного параметра выбираем функцию для сохранения изображения
            if self.save_format == 'const':
                captcha_id = await self.image_const_saver(content)
            elif self.save_format == 'temp':
                captcha_id = await self.image_temp_saver(content)
            else:
                return """Wrong 'save_format' parameter. Valid formats: 'const' or 'temp'.\n 
                        Неправильный 'save_format' параметр. Возможные форматы: 'const' или 'temp'."""

        else:
            return """You did not send any file local link or URL."""

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

        # Ожидаем решения капчи
        await asyncio.sleep(self.sleep_time)
        # отправляем запрос на результат решения капчи, если не решена ожидаем
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.post(url_response, data=self.get_payload) as resp:
                    captcha_response = await resp.json()

                    # если капча ещё не решена - ожидаем
                    if captcha_response['request'] == 'CAPCHA_NOT_READY':
                        time.sleep(self.sleep_time)

                    # при ошибке во время решения
                    elif captcha_response["status"] == 0:
                        self.result.update({'errorId': 1,
                                            'errorBody': RuCaptchaError().errors(captcha_response["request"])
                                            }
                                           )
                        return self.result

                    # при решении капчи
                    elif captcha_response["status"] == 1:
                        self.result.update({'errorId': 0,
                                            'captchaSolve': captcha_response['request']
                                            }
                                           )
                        return self.result
