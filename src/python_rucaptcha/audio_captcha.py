import base64
import shutil
from typing import Optional

from .core.base import BaseCaptcha
from .core.enums import SaveFormatsEnm, AudioCaptchaEnm


class AudioCaptcha(BaseCaptcha):
    def __init__(
        self,
        save_format: str = SaveFormatsEnm.TEMP.value,
        audio_clearing: bool = True,
        audio_path: str = "PythonRuCaptchaAudio",
        lang: str = "en",
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Text Captcha.

        Args:
            rucaptcha_key: User API key
            save_format: The format in which the file will be saved, or as a temporary file - 'temp',
                                 or as a regular file to a folder created by the library - 'const'.
            audio_clearing: True - delete file after solution, False - don't delete file after solution
            audio_path: Folder to save captcha audio
            lang: Captcha audio lang: `en`, `fr`, `de`, `el`, `pt`, `ru`

        Examples:
            >>> AudioCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             lang='en'
            ...             ).captcha_handler(captcha_file='examples/mediacaptcha_audio/recaptcha_55914.mp3')
            {
                'captchaSolve': 'five five nine one four',
                'taskId': 73243152973,
                'error': False,
                'errorBody': None
            }

            >>> await AudioCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             lang='en'
            ...             ).aio_captcha_handler(captcha_file='examples/mediacaptcha_audio/recaptcha_55914.mp3')
            {
                'captchaSolve': 'five five nine one four',
                'taskId': 73243152973,
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            https://rucaptcha.com/api-rucaptcha#audio
        """

        super().__init__(method=AudioCaptchaEnm.AUDIO.value, *args, **kwargs)
        self.save_format = save_format
        self.audio_clearing = audio_clearing
        self.audio_path = audio_path

        self.post_payload.update({"lang": lang})

    def captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        **kwargs,
    ) -> dict:
        """
        Synchronous method for captcha solving

        Args:
            captcha_link: Captcha file URL
            captcha_file: Captcha file path
            captcha_base64: Captcha file BASE64 info
            kwargs: additional params for `requests` library

        Examples:
            >>> AudioCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             lang='en'
            ...             ).captcha_handler(captcha_file='examples/mediacaptcha_audio/recaptcha_55914.mp3')
            {
                'captchaSolve': 'five five nine one four',
                'taskId': 73243152973,
                'error': False,
                'errorBody': None
            }

            >>> AudioCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             lang='en'
            ...             ).captcha_handler(captcha_link='http://some/link/address/recaptcha_55914.mp3')
            {
                'captchaSolve': 'five five nine one four',
                'taskId': 73243152973,
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        # if a local file link is passed
        if captcha_file:
            self.post_payload.update({"body": base64.b64encode(self._local_file_captcha(captcha_file)).decode("utf-8")})
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.post_payload.update({"body": base64.b64encode(captcha_base64).decode("utf-8")})
        # if a URL is passed
        elif captcha_link:
            try:
                content = self.url_open(url=captcha_link, **kwargs).content
            except Exception as error:
                self.result.error = True
                self.result.errorBody = str(error)
                return self.result.dict()

            # according to the value of the passed parameter, select the function to save the file
            if self.save_format == SaveFormatsEnm.CONST.value:
                self._file_const_saver(content, self.audio_path, file_extension="mp3")
            self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})

        else:
            # if none of the parameters are passed
            self.result.error = True
            self.result.errorBody = self.NO_CAPTCHA_ERR
            return self.result.dict()

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        **kwargs,
    ) -> dict:
        """
        Asynchronous method for captcha solving

        Args:
            captcha_link: Captcha file URL
            captcha_file: Captcha file path
            captcha_base64: Captcha file BASE64
            kwargs: additional params for `aiohttp` library

        Examples:
            >>> await AudioCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             lang='en'
            ...             ).aio_captcha_handler(captcha_file='examples/mediacaptcha_audio/recaptcha_55914.mp3')
            {
                'captchaSolve': 'five five nine one four',
                'taskId': 73243152973,
                'error': False,
                'errorBody': None
            }
            >>> await AudioCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             lang='en'
            ...             ).aio_captcha_handler(captcha_link='http://some/link/address/recaptcha_55914.mp3')
            {
                'captchaSolve': 'five five nine one four',
                'taskId': 73243152973,
                'error': False,
                'errorBody': None
            }

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        # if a local file link is passed
        if captcha_file:
            self.post_payload.update({"body": base64.b64encode(self._local_file_captcha(captcha_file)).decode("utf-8")})
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.post_payload.update({"body": base64.b64encode(captcha_base64).decode("utf-8")})
        # if a URL is passed
        elif captcha_link:
            try:
                content = await self.aio_url_read(url=captcha_link, **kwargs)
            except Exception as error:
                self.result.error = True
                self.result.errorBody = str(error)
                return self.result.dict()

            # according to the value of the passed parameter, select the function to save the file
            if self.save_format == SaveFormatsEnm.CONST.value:
                self._file_const_saver(content, self.audio_path, file_extension="mp3")
            self.post_payload.update({"body": base64.b64encode(content).decode("utf-8")})

        else:
            # if none of the parameters are passed
            self.result.error = True
            self.result.errorBody = self.NO_CAPTCHA_ERR
            return self.result.dict()

        return await self._aio_processing_response()

    def __del__(self):
        if self.save_format == SaveFormatsEnm.CONST.value and self.audio_clearing:
            shutil.rmtree(self.audio_path)
