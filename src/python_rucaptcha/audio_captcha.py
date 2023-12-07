import shutil
from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enums import SaveFormatsEnm, AudioCaptchaEnm
from .core.serializer import GetTaskResultResponseSer


class AudioCaptcha(BaseCaptcha):
    def __init__(
        self,
        save_format: Union[str, SaveFormatsEnm] = SaveFormatsEnm.TEMP,
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

            >>> with open("src/examples/mediacaptcha_audio/recaptcha_55914.mp3", "rb") as f:
            ...     file_data = f.read()
            >>> AudioCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122"
            ...             ).captcha_handler(captcha_base64=file_data)
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

            >>> with open("src/examples/mediacaptcha_audio/recaptcha_55914.mp3", "rb") as f:
            ...     file_data = f.read()
            >>> await AudioCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122"
            ...             ).aio_captcha_handler(captcha_base64=file_data)
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

        super().__init__(method=AudioCaptchaEnm.AudioTask.value, *args, **kwargs)
        self.save_format = save_format
        self.audio_clearing = audio_clearing
        self.audio_path = audio_path
        self.result = GetTaskResultResponseSer()

        self.create_task_payload["task"].update({"lang": lang})

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

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """

        self._body_file_processing(
            save_format=self.save_format,
            file_path=self.audio_path,
            file_extension="mp3",
            captcha_link=captcha_link,
            captcha_file=captcha_file,
            captcha_base64=captcha_base64,
            **kwargs,
        )
        if not self.result.errorId:
            return self._processing_response(**kwargs)
        return self.result.to_dict()

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

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        await self._aio_body_file_processing(
            save_format=self.save_format,
            file_path=self.audio_path,
            file_extension="mp3",
            captcha_link=captcha_link,
            captcha_file=captcha_file,
            captcha_base64=captcha_base64,
            **kwargs,
        )
        if not self.result.errorId:
            return await self._aio_processing_response()
        return self.result.to_dict()

    def __del__(self):
        if self.save_format == SaveFormatsEnm.CONST.value and self.audio_clearing:
            shutil.rmtree(self.audio_path)
