import os
import uuid
import base64
import shutil
import asyncio

import aiohttp

from . import enums
from .base import BaseCaptcha
from .serializer import CaptchaOptionsSer, ServicePostResponseSer
from .result_handler import get_async_result


class BaseImageCaptcha(BaseCaptcha):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class ImageCaptcha(BaseImageCaptcha):
    """
    The class is used to work with ImageCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_normal_captcha
    """

    def __init__(
        self,
        save_format: str = enums.SaveFormatsEnm.TEMP.value,
        img_clearing: bool = True,
        img_path: str = "PythonRuCaptchaImages",
        *args,
        **kwargs,
    ):
        """
        Initializing the necessary variables, creating a folder for images and cache
        After completion of work - temporary files and folders will be deleted
        :param save_format: The format in which the image will be saved, or as a temporary file - 'temp',
                             or as a regular image to a folder created by the library - 'const'.
        :param img_clearing: True - delete file after solution, False - don't delete file after solution;
        :param img_path: Folder to save captcha images;
        """
        super().__init__(*args, **kwargs)
        self.save_format = save_format
        self.img_clearing = img_clearing
        self.img_path = img_path

    def __image_const_saver(self, content: bytes):
        """
        Method create and save file in folder
        """
        # generate image name
        self._image_name = f"im-{uuid.uuid4()}.png"

        # save image to folder
        with open(os.path.join(self.img_path, self._image_name), "wb") as out_image:
            out_image.write(content)

    def __local_image_captcha(
        self,
        content: str,
    ):
        """
        Method get local image, read it and prepare for sending to Captcha solving service
        """
        with open(content, "rb") as captcha_image:
            return captcha_image.read()

    def captcha_handler(
        self,
        captcha_link: str = None,
        captcha_file: str = None,
        captcha_base64: bytes = None,
        **kwargs,
    ) -> dict:
        """
        The method is responsible for sending data to the server to solve the captcha
        :param captcha_link: Captcha image URL
        :param captcha_file: Captcha image file
        :param captcha_base64: Captcha image BASE64 info
        :param kwargs: Parameters for the `requests` library
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        # if a local file link is passed
        if captcha_file:
            self.__local_image_captcha(captcha_file)
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.post_payload.update({"body": base64.b64encode(captcha_base64).decode("utf-8")})
        # if a URL is passed
        elif captcha_link:
            try:
                content = self.url_open(url=captcha_link, **kwargs).content
            except Exception as error:
                self.result.error = True
                self.result.errorBody = error
                return self.result.dict(exclude_none=True)

            # according to the value of the passed parameter, select the function to save the image
            if self.save_format == enums.SaveFormatsEnm.CONST.value:
                self.__image_const_saver(content)
            self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})

        else:
            # if none of the parameters are passed
            self.result.error = True
            self.result.errorBody = "You did not send any file, local link or URL."
            return self.result.dict(exclude_none=True)

        return self._processing_response(**kwargs)

    def __del__(self):
        if self.save_format == enums.SaveFormatsEnm.CONST.value and self.img_clearing:
            shutil.rmtree(self.img_path)


class aioImageCaptcha(BaseCaptcha):
    """
    Данный асинхронный класс подходит для решения капчи-изображения.
    """

    def __init__(
        self,
        rucaptcha_key: str,
        sleep_time: int = 5,
        save_format: str = enums.SaveFormatsEnm.TEMP.value,
        service_type: str = enums.ServicesEnm.TWOCAPTCHA.value,
        img_clearing: bool = True,
        img_path: str = "PythonRuCaptchaImages",
        **kwargs,
    ):
        """
        Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удалются временные фалйы и папки
        :param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
        :param save_format: Формат в котором будет сохраняться изображение,
                        либо как временный фпйл - 'temp',
                        либо как обычное изображение в папку созданную библиотекой - 'const'.
        :param service_type: URL с которым будет работать программа,
                        возможен вариант "2captcha"(стандартный) и "rucaptcha"
        :param img_path: Папка для сохранения изображений капчи;
        :param img_clearing: True - удалять файл после решения,
                            False - не удалять файл после решения;
        :param kwargs: Служит для передачи необязательных параметров
                        в пайлоад для запроса к RuCaptcha
            Подробнее о параметрах:
                https://rucaptcha.com/api-rucaptcha#solving_normal_captcha

        Подробней с примерами можно ознакомиться в 'CaptchaTester/image_captcha_example.py'
        """
        super().__init__(rucaptcha_key, sleep_time, service_type, **kwargs)
        # assign args to validator
        self.params = CaptchaOptionsSer(**locals())

    async def __image_temp_saver(self, content: bytes):
        """
        Метод отправляет капчу сразу на сервер для расшифровки.
        :return: Возвращает ID капчи из сервиса
        """

        try:
            self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url_request, data=self.post_payload) as resp:
                    response_json = await resp.json()
                    response = ServicePostResponseSer(**response_json)

            if response.status == 1:
                self.result.taskId = response.request
            else:
                self.result.error = True
                self.result.errorBody = response.request

        except Exception as error:
            self.result.error = True
            self.result.errorBody = error

    async def __image_const_saver(self, content: bytes):
        """
        Метод создаёт папку и сохраняет в неё изображение
        :return: Возвращает ID капчи из сервиса
        """
        try:
            # уникальное имя изображения
            image_name = uuid.uuid4()

            with open(os.path.join(self.img_path, f"im-{image_name}.png"), "wb") as out_image:
                out_image.write(content)

            self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url_request, data=self.post_payload) as resp:
                    response_json = await resp.json()
                    response = ServicePostResponseSer(**response_json)

            if response.status == 1:
                self.result.taskId = response.request
            else:
                self.result.error = True
                self.result.errorBody = response.request

        except Exception as error:
            self.result.error = True
            self.result.errorBody = error

    async def __local_image_captcha(self, content: str, content_type: str = "file"):
        """
        Метод получает в качестве параметра ссылку на локальный файл
            (или файл в кодировке base64)
        для проверки и получения её ID
        :param content: Ссылка на локальный файл
        :param content_type: Тип передаваемого файла,
                    может быть `file`(если передан локальный адрес) или
                    `base64`(если передано изображение в кодировке base64)
        :return: ID капчи в сервисе
        """
        try:
            if content_type == "file":
                with open(content, "rb") as captcha_image:
                    # Отправляем на рукапча изображение капчи и другие парметры
                    self.post_payload.update({"body": base64.b64encode(captcha_image.read()).decode("utf-8")})

            elif content_type == "base64":
                self.post_payload.update({"body": content})

            else:
                raise ValueError(f"Wrong content type passed! Valid: `file` and `base64`. You passed: `{content_type}`")

            async with aiohttp.ClientSession() as session:
                async with session.post(self.url_request, data=self.post_payload) as resp:
                    response_json = await resp.json()
                    response = ServicePostResponseSer(**response_json)

            if response.status == 1:
                self.result.taskId = response.request
            else:
                self.result.error = True
                self.result.errorBody = response.request

        except Exception as error:
            self.result.error = True
            self.result.errorBody = error

    async def captcha_handler(
        self,
        captcha_link: str = None,
        captcha_file: str = None,
        captcha_base64: str = None,
        proxy: str = None,
    ) -> dict:
        """
        Метод получает от вас капчу и отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
        :param captcha_file: Адрес(локальный) по которому находится изображение
                                для отправки на расшифровку
        :param captcha_base64: Изображение переданное в кодировке base64
        :param proxy: Прокси для aiohttp модуля
        :return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    taskId - находится Id задачи на решение капчи,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - название ошибки
        """
        # if a local file link is passed
        if captcha_file:
            await self.__local_image_captcha(captcha_file)
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            await self.__local_image_captcha(captcha_base64, content_type="base64")
        # if a URL is passed
        elif captcha_link:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=captcha_link, proxy=proxy) as resp:
                        content = await resp.content.read()
            except Exception as error:
                self.result.error = True
                self.result.errorBody = error
                return self.result.dict(exclude_none=True)

            # according to the value of the passed parameter, select the function to save the image
            if self.save_format == enums.SaveFormatsEnm.CONST.value:
                await self.__image_const_saver(content)
            elif self.save_format == enums.SaveFormatsEnm.TEMP.value:
                await self.__image_temp_saver(content)

        else:
            # if none of the parameters are passed
            self.result.error = True
            self.result.errorBody = "You did not send any file, local link or URL."
            return self.result.dict(exclude_none=True)
        # check for errors when downloading / transferring a file to the server
        if self.result.error:
            return self.result.dict(exclude_none=True)
        # if all is ok - send captcha to service and wait solution
        else:
            # update payload - add captcha taskId
            self.get_payload.update({"id": self.result.taskId})

            # wait captcha solving
            await asyncio.sleep(self.sleep_time)
            return await get_async_result(
                get_payload=self.get_payload,
                sleep_time=self.sleep_time,
                url_response=self.url_response,
                result=self.result,
            )

    def __del__(self):
        if self.save_format == enums.SaveFormatsEnm.CONST.value and self.img_clearing:
            shutil.rmtree(self.img_path)


'''
class sockNormalCaptcha(WebSocketRuCaptcha):
    """
    Class for ImageCaptcha
    """

    def __init__(self, rucaptcha_key: str, allSessions: bool = None, suppressSuccess: bool = None):
        """
        Method setup WebSocket connection data
        """
        super().__init__(allSessions, suppressSuccess)
        self.rucaptcha_key = rucaptcha_key

    async def captcha_handler(self, captcha_image_base64: str, **kwargs) -> dict:
        """
        The asynchronous WebSocket method return account balance.
        More info - https://wsrucaptcha.docs.apiary.io/#reference/text-captcha
        :param captcha_image_base64: Image captcha base64 data in string format (decoded in utf-8)
        :param kwargs: Options variables
        :return: Server response dict
        """
        normal_captcha_payload = NormalCaptchaSocketSer(
            **{
                "method": "normal",
                "requestId": str(uuid4()),
                "body": captcha_image_base64,
                "options": CaptchaOptionsSocketSer(**kwargs),
            }
        )

        return await self.send_request(normal_captcha_payload.dict())
'''
