import base64
import asyncio

from .base import BaseCaptcha
from .enums import RotateCaptchaEnm


class BaseRotateCaptcha(BaseCaptcha):
    def __init__(self, method: str = RotateCaptchaEnm.ROTATECAPTCHA.value, *args, **kwargs):
        super().__init__(method=method, *args, **kwargs)

        # check user params
        if method not in RotateCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {RotateCaptchaEnm.list_values()}")


class RotateCaptcha(BaseRotateCaptcha):
    """
    The class is used to work with RotateCaptcha
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_rotatecaptcha
    """

    def captcha_handler(self, captcha_link: str, **kwargs):
        """
        The method is responsible for sending data to the server to solve the captcha
        :param captcha_link: link or path to captcha file
        :param kwargs: Parameters for the `requests` library
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        # if user send link - download file
        if "http" in captcha_link:
            content: bytes = self.session.get(captcha_link).content
        # is user send file path - read ir
        else:
            with open(captcha_link, "rb") as captcha_image:
                content: bytes = captcha_image.read()
        # decode file data in base64 and prepare payload
        self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})

        return self._processing_response(**kwargs)


class aioRotateCaptcha:
    """
    The class is used to async work with RotateCaptcha
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_rotatecaptcha
    """

    async def captcha_handler(self, captcha_link: str, **kwargs):
        """
        Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
        :param kwargs: Для передачи дополнительных параметров
        :return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - название ошибки
        """
        # result, url_request, url_response - задаются в декораторе `service_check`, после проверки переданного названия

        # Если переданы ещё параметры - вносим их в get_payload
        if kwargs:
            for key in kwargs:
                self.get_payload.update({key: kwargs[key]})

        # Скачиваем изображение
        content = self.session.get(captcha_link).content

        # Отправляем изображение файлом
        self.post_payload.update({"file": content})
        # получаем ID капчи
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url_request, data=self.post_payload) as resp:
                captcha_id = await resp.json()

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id["status"] == 0:
            self.result.update({"error": True, "errorBody": captcha_id["request"]})
            return self.result
        # иначе берём ключ отправленной на решение капчи и ждём решения
        else:
            captcha_id = captcha_id["request"]
            # вписываем в taskId ключ отправленной на решение капчи
            self.result.update({"taskId": captcha_id})
            # обновляем пайлоад, вносим в него ключ отправленной на решение капчи
            self.get_payload.update({"id": captcha_id})

            # если передан параметр `pingback` - не ждём решения капчи а возвращаем незаполненный ответ
            if self.post_payload.get("pingback"):
                return self.get_payload

            else:
                # Ожидаем решения капчи
                await asyncio.sleep(self.sleep_time)
                return await get_async_result(
                    get_payload=self.get_payload,
                    sleep_time=self.sleep_time,
                    url_response=self.url_response,
                    result=self.result,
                )
