import os
import uuid
import base64
import shutil

from python_rucaptcha.core.base import BaseCaptcha
from python_rucaptcha.core.enums import SaveFormatsEnm, ImageCaptchaEnm


class BaseImageCaptcha(BaseCaptcha):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(method=ImageCaptchaEnm.BASE64.value, *args, **kwargs)

    def _image_const_saver(self, content: bytes, img_path: str):
        """
        Method create and save file in folder
        """
        # generate image name
        self._image_name = f"im-{uuid.uuid4()}.png"

        # save image to folder
        with open(os.path.join(img_path, self._image_name), "wb") as out_image:
            out_image.write(content)

    @staticmethod
    def _local_image_captcha(captcha_file: str):
        """
        Method get local image, read it and prepare for sending to Captcha solving service
        """
        with open(captcha_file, "rb") as file:
            return file.read()


class ImageCaptcha(BaseImageCaptcha):
    """
    The class is used to work with ImageCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_normal_captcha
    """

    def __init__(
        self,
        save_format: str = SaveFormatsEnm.TEMP.value,
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
        :param captcha_file: Captcha image file path
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
            self.post_payload.update(
                {"body": base64.b64encode(self._local_image_captcha(captcha_file)).decode("utf-8")}
            )
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
            if self.save_format == SaveFormatsEnm.CONST.value:
                self._image_const_saver(content, self.img_path)
            self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})

        else:
            # if none of the parameters are passed
            self.result.error = True
            self.result.errorBody = "You did not send any file, local link or URL."
            return self.result.dict(exclude_none=True)

        return self._processing_response(**kwargs)

    def __del__(self):
        if self.save_format == SaveFormatsEnm.CONST.value and self.img_clearing:
            shutil.rmtree(self.img_path)


class aioImageCaptcha(BaseImageCaptcha):
    """
    The class is used to async work with ImageCaptcha.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#solving_normal_captcha
    """

    def __init__(
        self,
        save_format: str = SaveFormatsEnm.TEMP.value,
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

    async def captcha_handler(
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
        :param kwargs: Additional parameters for the `aiohttp` library
        :return: Response to captcha as JSON string with fields:
                 captchaSolve - captcha solution,
                 taskId - finds the ID of the task to solve the captcha,
                 error - False - if everything is fine, True - if there is an error,
                 errorBody - error name
        """
        # if a local file link is passed
        if captcha_file:
            self.post_payload.update(
                {"body": base64.b64encode(self._local_image_captcha(captcha_file)).decode("utf-8")}
            )
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.post_payload.update({"body": base64.b64encode(captcha_base64).decode("utf-8")})
        # if a URL is passed
        elif captcha_link:
            try:
                content = await self.aio_url_read(url=captcha_link, **kwargs)
            except Exception as error:
                self.result.error = True
                self.result.errorBody = error
                return self.result.dict(exclude_none=True)

            # according to the value of the passed parameter, select the function to save the image
            if self.save_format == SaveFormatsEnm.CONST.value:
                self._image_const_saver(content, self.img_path)
            self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})

        else:
            # if none of the parameters are passed
            self.result.error = True
            self.result.errorBody = "You did not send any file, local link or URL."
            return self.result.dict(exclude_none=True)

        return await self._aio_processing_response()

    def __del__(self):
        if self.save_format == SaveFormatsEnm.CONST.value and self.img_clearing:
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
