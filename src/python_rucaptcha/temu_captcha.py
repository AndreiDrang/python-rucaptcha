import shutil
from typing import Any, Union

from .core.base import BaseCaptcha
from .core.enums import SaveFormatsEnm, TemuCaptchaEnm


class TemuCaptcha(BaseCaptcha):
    def __init__(
        self,
        save_format: Union[str, SaveFormatsEnm] = SaveFormatsEnm.TEMP,
        img_clearing: bool = True,
        img_path: str = "PythonRuCaptchaImages",
        *args,
        **kwargs: dict[str, Any],
    ):
        """
        Solve TemuImageTask CAPTCHA via 2Captcha/RuCaptcha API.

        This class creates and monitors TemuImageTask jobs, which require
        a base64‐encoded background image plus an array of movable image
        pieces (parts) in base64 format.  It extends BaseCaptcha to handle
        the low‐level request/response workflow.

        Args:
            save_format (str | SaveFormatsEnm): Where to save temporary images.
                - SaveFormatsEnm.TEMP: use system temp directory
                - SaveFormatsEnm.CONST: keep files in img_path until deletion
            img_clearing (bool): If True and save_format is CONST, delete the
                img_path directory when this instance is destroyed.
            img_path (str): Directory under which to store downloaded or decoded
                images before sending to the API.
            *args: Positional args forwarded to BaseCaptcha constructor (e.g.
                client_key, method override).
            **kwargs: Keyword args forwarded to BaseCaptcha for task creation.
                Common params include:
                - redirectUri: URL to confirm CAPTCHA resolution
                - any other API‐supported parameters

        Examples:
            >>> captcha = TemuCaptcha(rucaptcha_key="YOUR_API_KEY")
            >>> response = captcha.captcha_handler(
            ...     parts=["part1_b64", "part2_b64", "part3_b64"],
            ...     captcha_base64=b"full_image_b64"
            ... )
            >>> print(response)
            {
                "errorId": 0,
                "status": "ready",
                "solution": {
                    "coordinates": [{"x":155,"y":358}, {"x":152,"y":153}, {"x":251,"y":333}]
                },
                "cost": "0.0012",
                "createTime": 1754563182,
                "endTime": 1754563190,
                "taskId": 80306543329,
                "ip": "46.53.232.76",
                "solveCount": 1
            }

        Notes:
            https://2captcha.com/api-docs/temu-captcha

            https://rucaptcha.com/api-docs/temu-captcha
        """
        super().__init__(method=TemuCaptchaEnm.TemuCaptchaTask, *args, **kwargs)

        self.save_format = save_format
        self.img_clearing = img_clearing
        self.img_path = img_path

    def captcha_handler(
        self,
        parts: list[str],
        captcha_link: str | None = None,
        captcha_file: str | None = None,
        captcha_base64: bytes | None = None,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Synchronously solve a TemuImageTask.

        Args:
            parts (list[str]): List of base64‐encoded strings for each
                movable image piece.
            captcha_link (str | None): URL to background image. Overrides
                captcha_file and captcha_base64 if provided.
            captcha_file (str | None): Path to an image file to read & send.
            captcha_base64 (bytes | None): Raw bytes or base64 string of
                the background image.
            **kwargs: Passed through to the HTTP request call (e.g. timeout,
                headers).

        Returns:
            dict[str, Any]: Full JSON response from the 2Captcha/RuCaptcha API,
                including errorId, taskId, status, solution, cost, times, etc.
        """
        self.create_task_payload["task"].update({"parts": parts})
        self._body_file_processing(
            save_format=self.save_format,
            file_path=self.img_path,
            captcha_link=captcha_link,
            captcha_file=captcha_file,
            captcha_base64=captcha_base64,
            image_key="image",
            **kwargs,
        )
        if not self.result.errorId:
            return self._processing_response(**kwargs)
        return self.result.to_dict()

    async def aio_captcha_handler(
        self,
        parts: list[str],
        captcha_link: str | None = None,
        captcha_file: str | None = None,
        captcha_base64: bytes | None = None,
    ) -> dict[str, Any]:
        """
        Asynchronously solve a TemuImageTask.

        Args:
            parts (list[str]): List of base64‐encoded strings for each
                movable image piece.
            captcha_link (str | None): URL to background image.
            captcha_file (str | None): Path to an image file to read & send.
            captcha_base64 (bytes | None): Raw bytes or base64 string of image.
            **kwargs: Passed through to the async HTTP request call.

        Returns:
            dict[str, Any]: API response containing task status and solution.
        """
        self.create_task_payload["task"].update({"parts": parts})
        await self._aio_body_file_processing(
            save_format=self.save_format,
            file_path=self.img_path,
            captcha_link=captcha_link,
            captcha_file=captcha_file,
            captcha_base64=captcha_base64,
            image_key="image",
            **kwargs,
        )
        if not self.result.errorId:
            return await self._aio_processing_response()
        return self.result.to_dict()

    def __del__(self):
        """
        Cleanup saved images folder if configured to do so.
        """
        if self.save_format == SaveFormatsEnm.CONST.value and self.img_clearing:
            shutil.rmtree(self.img_path)
