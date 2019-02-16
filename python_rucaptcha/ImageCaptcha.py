import requests
import time
import shutil
import os
import asyncio
import aiohttp
import base64
from requests.adapters import HTTPAdapter

from python_rucaptcha.config import app_key
from python_rucaptcha.errors import RuCaptchaError
from python_rucaptcha.result_handler import get_sync_result, get_async_result
from python_rucaptcha.decorators import api_key_check, service_check


class ImageCaptcha:
    """
    Данный метод подходит как для загрузки и решения обычной капчи
    так и для большой капчи.
    Требуется передать API ключ сайта, ссылку на изображение и,по желанию, время ожидания решения капчи
    Подробней информацию смотрите в методе 'captcha_handler'
    """

    def __init__(self, rucaptcha_key: str, sleep_time: int = 5, save_format: str = 'temp',
                 service_type: str = '2captcha', img_clearing: bool = True, img_path: str = 'PythonRuCaptchaImages',
                 **kwargs):
        """
        Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удалются временные фалйы и папки
        :param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
        :param save_format: Формат в котором будет сохраняться изображение, либо как временный фпйл - 'temp',
                            либо как обычное изображение в папку созданную библиотекой - 'const'.
        :param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        :param img_path: Папка для сохранения изображений капчи;
        :param img_clearing: True - удалять файл после решения, False - не удалять файл после решения;
        :param kwargs: Служит для передачи необязательных параметров в пайлоад для запроса к RuCaptcha

        Подробней с примерами можно ознакомиться в 'CaptchaTester/image_captcha_example.py'
        """
        # время ожидания решения капчи
        self.sleep_time = sleep_time
        # тип URL на с которым будет работать библиотека
        self.service_type = service_type

        # проверяем переданный параметр способа сохранения капчи
        if save_format in ['const', 'temp']:
            self.save_format = save_format
            # если файл сохраняется в папку, берём параметр названия папки и очистк/не очистки папки от капч
            if self.save_format == 'const':
                # очищаем папку после решения капчи - True, сохраняем все файлы - False
                self.img_clearing = img_clearing
                # название папки для сохранения файлов капчи
                self.img_path = img_path
                # создаём папку для сохранения капч
                os.makedirs(self.img_path, exist_ok=True)

        else:
            raise ValueError('\nПередан неверный формат сохранения файла изображения. '
                             f'\n\tВозможные варинты: `temp` и `const`. Вы передали - `{save_format}`'
                             '\nWrong `save_format` parameter. Valid params: `const` or `temp`.'
                             f'\n\tYour param - `{save_format}`')

        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             "method": "base64",
                             "json": 1,
                             "soft_id": app_key,
                             }
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
        self.session.mount('http://', HTTPAdapter(max_retries = 5))
        self.session.mount('https://', HTTPAdapter(max_retries = 5))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    def __image_temp_saver(self, content: bytes):
        """
        Метод сохраняет файл изображения как временный и отправляет его сразу на сервер для расшифровки.
        :return: Возвращает ID капчи из сервиса
        """
        captcha_id = None
        try:
            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            self.post_payload.update({"body": base64.b64encode(content).decode('utf-8')})
            captcha_id = self.session.post(self.url_request, data = self.post_payload).json()

        except Exception as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )

        finally:
            return captcha_id

    def __image_const_saver(self, content: bytes):
        """
        Метод создаёт папку и сохраняет в неё изображение, затем передаёт его на расшифровку и удалет файл.
        :param content: Файл для сохранения;
        :return: Возвращает ID капчи из сервиса
        """
        captcha_id = None

        try:
            # Высчитываем хэш изображения, для того что бы сохранить его под уникальным именем
            image_hash = hash(content)

            # сохраняем в папку изображение
            with open(os.path.join(self.img_path, f'im-{image_hash}.png'), 'wb') as out_image:
                out_image.write(content)

            with open(os.path.join(self.img_path, f'im-{image_hash}.png'), 'rb') as captcha_image:
                # Отправляем на рукапча изображение капчи и другие парметры,
                # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
                self.post_payload.update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
                captcha_id = self.session.post(self.url_request, data = self.post_payload).json()

        except (IOError, FileNotFoundError) as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )

        except Exception as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )

        finally:

            return captcha_id

    def __local_image_captcha(self, content: str, content_type: str = "file"):
        """
        Метод получает в качестве параметра ссылку на локальный файл(или файл в кодировке base64), считывает изображение и отправляет его на РуКапчу
        для проверки и получения её ID
        :param content: Ссылка на локальный файл
        :param content_type: Тип передаваемого файла, Может быть `file`(если передан локальный адрес) или
                            `base64`(если передано изображение в кодировке base64)
        :return: ID капчи в сервисе
        """
        captcha_id = None

        try:
            # пробуем открыть файл, закодировать в base64, затем вносим закодированный файл в post_payload для отправки на
            # рукапчу для решения
            if content_type == 'file':
                with open(content, 'rb') as captcha_image:
                    self.post_payload.update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})

            # вносим закодированный файл в post_payload для отправки на рукапчу для решения
            elif content_type == "base64":
                self.post_payload.update({"body": content})

            else:
                raise ValueError(f'Передан неверный тип контента! Допустимые: `file` и `base64`. '
                                 f'Вы передали: `{content_type}`')

            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            captcha_id = self.session.post(self.url_request, data = self.post_payload).json()

        except (IOError, FileNotFoundError) as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )

        except Exception as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )

        finally:
            return captcha_id

    @api_key_check
    @service_check
    def captcha_handler(self, captcha_link: str = None, captcha_file: str = None, captcha_base64: str = None, **kwargs):
        """
        Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
        :param captcha_file: Адрес(локальный) по которому находится изображение для отправки на расшифровку
        :param captcha_base64: Изображение переданное в кодировке base64
        :param kwargs: Параметры для библиотеки `requests`
        :return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - полная информация об ошибке:
                        {
                            text - Развернётое пояснение ошибки
                            id - уникальный номер ошибка в ЭТОЙ бибилотеке
                        }
        """
        # result, url_request, url_response - задаются в декораторе `service_check`, после проверки переданного названия
        
        # если передана локальная ссылка на файл
        if captcha_file:
            captcha_id = self.__local_image_captcha(captcha_file)
        # если передан файл в кодировке base64
        elif captcha_base64:
            captcha_id = self.__local_image_captcha(captcha_base64, content_type = "base64")
        # если передан URL
        elif captcha_link:
            try:
                content = self.session.get(url = captcha_link, **kwargs).content
            except Exception as error:
                self.result.update({'error': True,
                                    'errorBody': {
                                        'text': error,
                                        'id': -1
                                        }
                                    }
                                   )
                return self.result

            # согласно значения переданного параметра выбираем функцию для сохранения изображения
            if self.save_format == 'const':
                captcha_id = self.__image_const_saver(content)
            elif self.save_format == 'temp':
                captcha_id = self.__image_temp_saver(content)

        else:
            # если не передан ни один из параметров
            self.result.update({'error': True,
                                'errorBody': 'You did not send any file local link or URL.',
                                }
                               )
            return self.result
        # проверяем наличие ошибок при скачивании/передаче файла на сервер
        if self.result['error']:
            return self.result

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        elif captcha_id['status'] == 0:
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

    def __del__(self):
        if self.save_format == 'const':
            if self.img_clearing:
                shutil.rmtree(self.img_path)


class aioImageCaptcha:
    """
    Данный асинхронный метод подходит как для загрузки и решения обычной капчи
    так и для большой капчи.
    Требуется передать API ключ сайта, ссылку на изображение и,по желанию, время ожидания решения капчи
    Подробней информацию смотрите в методе 'captcha_handler'
    """

    def __init__(self, rucaptcha_key: str, sleep_time: int = 5, save_format: str = 'temp',
                 service_type: str = '2captcha', img_clearing: bool = True, img_path: str = 'PythonRuCaptchaImages',
                 **kwargs):
        """
        Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удалются временные фалйы и папки
        :param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
        :param save_format: Формат в котором будет сохраняться изображение, либо как временный фпйл - 'temp',
                            либо как обычное изображение в папку созданную библиотекой - 'const'.
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
        :param img_path: Папка для сохранения изображений капчи;
        :param img_clearing: True - удалять файл после решения, False - не удалять файл после решения;
        :param kwargs: Служит для передачи необязательных параметров в пайлоад для запроса к RuCaptcha

        Подробней с примерами можно ознакомиться в 'CaptchaTester/image_captcha_example.py'
        """
        # время ожидания решения капчи
        self.sleep_time = sleep_time
        # тип URL на с которым будет работать библиотека
        self.service_type = service_type

        # проверяем переданный параметр способа сохранения капчи
        if save_format in ['const', 'temp']:
            self.save_format = save_format
            # если файл сохраняется в папку, берём параметр названия папки и очистк/не очистки папки от капч
            if self.save_format == 'const':
                # очищаем папку после решения капчи - True, сохраняем все файлы - False
                self.img_clearing = img_clearing
                # название папки для сохранения файлов капчи
                self.img_path = img_path
                # создаём папку для сохранения капч
                os.makedirs(self.img_path, exist_ok=True)
        else:
            raise ValueError('\nПередан неверный формат сохранения файла изображения. '
                             f'\n\tВозможные варинты: `temp` и `const`. Вы передали - `{save_format}`'
                             '\nWrong `save_format` parameter. Valid params: `const` or `temp`.'
                             f'\n\tYour param - `{save_format}`')

        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             "method": "base64",
                             "json": 1,
                             "soft_id": app_key,
                             }
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

    async def __image_temp_saver(self, content: bytes):
        """
        Метод сохраняет файл изображения как временный и отправляет его сразу на сервер для расшифровки.
        :return: Возвращает ID капчи из сервиса
        """
        captcha_id = None

        try:
            self.post_payload.update({"body": base64.b64encode(content).decode('utf-8')})
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url_request, data = self.post_payload) as resp:
                    captcha_id = await resp.json()

        except Exception as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )

        finally:
            return captcha_id

    async def __image_const_saver(self, content: bytes):
        """
        Метод создаёт папку и сохраняет в неё изображение, затем передаёт его на расшифровку и удалет файл.
        :return: Возвращает ID капчи из сервиса
        """
        captcha_id = None
        try:
            # Высчитываем хэш изображения, для того что бы сохранить его под уникальным именем
            image_hash = hash(content)

            with open(os.path.join(self.img_path, f'im-{image_hash}.png'), 'wb') as out_image:
                out_image.write(content)

            with open(os.path.join(self.img_path, f'im-{image_hash}.png'), 'rb') as captcha_image:
                # Отправляем на рукапча изображение капчи и другие парметры,
                # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
                self.post_payload.update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.url_request, data = self.post_payload) as resp:
                        captcha_id = await resp.json()

        except (IOError, FileNotFoundError) as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )

        except Exception as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )
        finally:
            return captcha_id

    async def __local_image_captcha(self, content: str, content_type: str = 'file'):
        """
        Метод получает в качестве параметра ссылку на локальный файл(или файл в кодировке base64), считывает изображение и отправляет его на РуКапчу
        для проверки и получения её ID
        :param content: Ссылка на локальный файл
        :param content_type: Тип передаваемого файла, Может быть `file`(если передан локальный адрес) или
                            `base64`(если передано изображение в кодировке base64)
        :return: ID капчи в сервисе
        """
        captcha_id = None

        try:
            if content_type == 'file':
                with open(content, 'rb') as captcha_image:
                    # Отправляем на рукапча изображение капчи и другие парметры,
                    # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
                    self.post_payload.update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})

            elif content_type == "base64":
                self.post_payload.update({"body": content})

            else:
                raise ValueError(f'Передан неверный тип контента! Допустимые: `file` и `base64`. '
                                 f'Вы передали: `{content_type}`')

            captcha_id = requests.post(self.url_request, data = self.post_payload).json()

        except (IOError, FileNotFoundError) as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )

        except Exception as error:
            self.result.update({'error': True,
                                'errorBody': {
                                    'text': error,
                                    'id': -1
                                    }
                                }
                               )
        finally:
            return captcha_id

    @api_key_check
    @service_check
    async def captcha_handler(self, captcha_link: str = None, captcha_file: str = None, captcha_base64: str = None,
                              proxy: str = None):
        """
        Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
        :param captcha_file: Адрес(локальный) по которому находится изображение для отправки на расшифровку
        :param captcha_base64: Изображение переданное в кодировке base64
        :param proxy: Прокси для aiohttp модуля
        :return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - полная информация об ошибке:
                        {
                            text - Развернётое пояснение ошибки
                            id - уникальный номер ошибка в ЭТОЙ бибилотеке
                        }
        """
        # result, url_request, url_response - задаются в декораторе `service_check`, после проверки переданного названия

        # если передана локальная ссылка на файл - работаем с ним
        if captcha_file:
            captcha_id = await self.__local_image_captcha(captcha_file)
        # если передан файл в кодировке base64
        elif captcha_base64:
            captcha_id = await self.__local_image_captcha(captcha_base64, content_type="base64")
        elif captcha_link:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url = captcha_link, proxy = proxy) as resp:
                        content = await resp.content.read()
            except Exception as error:
                self.result.update({'error': True,
                                    'errorBody': {
                                        'text': error,
                                        'id': -1
                                        }
                                    }
                                   )
                return self.result

            # согласно значения переданного параметра выбираем функцию для сохранения изображения
            if self.save_format == 'const':
                captcha_id = await self.__image_const_saver(content)
            elif self.save_format == 'temp':
                captcha_id = await self.__image_temp_saver(content)

        else:
            self.result.update({'error': True,
                                'errorBody': 'You did not send any file local link or URL.',
                                }
                               )
            return self.result

        # проверяем наличие ошибок при скачивании/передаче файла на сервер
        if self.result['error']:
            return self.result

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        elif captcha_id['status'] == 0:
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

    def __del__(self):
        if self.save_format == 'const':
            if self.img_clearing:
                shutil.rmtree(self.img_path)
