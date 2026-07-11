from typing import Any, Union, Optional

from .core.base import BaseCaptcha
from .core.enums import VKCaptchaEnm, SaveFormatsEnm


class VKCaptcha(BaseCaptcha):
    def __init__(
        self,
        method: Union[str, VKCaptchaEnm] = VKCaptchaEnm.VKCaptchaImageTask,
        redirectUri: Optional[str] = None,
        userAgent: Optional[str] = None,
        proxyType: Optional[str] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        save_format: Union[str, SaveFormatsEnm] = SaveFormatsEnm.TEMP,
        img_path: str = "PythonRuCaptchaImages",
        *args,
        **kwargs,
    ):
        """
        The class is used to work with VKCaptchaTask and VKCaptchaImageTask.

        VKCaptchaTask requires proxy and returns a token.
        VKCaptchaImageTask takes a captcha image and steps, returns image solution.

        Args:
            rucaptcha_key: User API key
            method: Captcha type - VKCaptchaTask or VKCaptchaImageTask
            redirectUri: The URL that is returned on requests to the captcha API (VKCaptchaTask)
            userAgent: User-Agent of your browser will be used to load the captcha (VKCaptchaTask)
            proxyType: Proxy type - http, https, socks5 (VKCaptchaTask)
            proxyAddress: Proxy IP address or hostname (VKCaptchaTask)
            proxyPort: Proxy port (VKCaptchaTask)
            proxyLogin: Proxy login (VKCaptchaTask)
            proxyPassword: Proxy password (VKCaptchaTask)
            save_format: Image save format for VKCaptchaImageTask - 'temp' or 'const'
            img_path: Folder to save captcha images for VKCaptchaImageTask
            kwargs: Not required params for task creation request

        Examples:
            >>> VKCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             redirectUri="https://id.vk.com/not_robot_captcha?domain=vk.com...",
            ...             userAgent="Mozilla/5.0 .....",
            ...             proxyType="socks5",
            ...             proxyAddress="1.2.3.4",
            ...             proxyPort=445,
            ...             ).captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"142000f.....er"
               },
               "cost":"0.002",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":0,
               "taskId": 73243152973,
            }

            >>> await VKCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             redirectUri="https://id.vk.com/not_robot_captcha?domain=vk.com...",
            ...             userAgent="Mozilla/5.0 .....",
            ...             proxyType="socks5",
            ...             proxyAddress="1.2.3.4",
            ...             proxyPort=445,
            ...             ).aio_captcha_handler()
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "token":"142000f.....er"
               },
               "cost":"0.002",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":0,
               "taskId": 73243152973,
            }

            >>> VKCaptcha(rucaptcha_key="aa9011f31111181111168611f1151122",
            ...             method=VKCaptchaEnm.VKCaptchaImageTask,
            ...             ).captcha_handler(
            ...                 captcha_link="https://example.com/vk_captcha.png", steps=[3, 4, 5]
            ...             )
            {
               "errorId":0,
               "status":"ready",
               "solution":{
                  "best_step": 1,
                  "preview": "...",
                  "solution": "...",
                  "answer": "..."
               },
               "cost":"0.002",
               "ip":"1.2.3.4",
               "createTime":1692863536,
               "endTime":1692863556,
               "solveCount":0,
               "taskId": 73243152973,
            }

        Returns:
            Dict with full server response

        Notes:
            https://2captcha.com/api-docs/vk-captcha

            https://rucaptcha.com/api-docs/vk-captcha
        """
        super().__init__(method=method, *args, **kwargs)

        if method not in VKCaptchaEnm.list_values():
            raise ValueError(f"Invalid method parameter set, available - {VKCaptchaEnm.list_values()}")

        self.method = method
        self.save_format = save_format
        self.img_path = img_path

        if method == VKCaptchaEnm.VKCaptchaTask:
            if not all([redirectUri, userAgent, proxyType, proxyAddress, proxyPort]):
                raise ValueError(
                    "redirectUri, userAgent, proxyType, proxyAddress, "
                    "and proxyPort are required for VKCaptchaTask"
                )

            task_data = {
                "redirectUri": redirectUri,
                "userAgent": userAgent,
                "proxyType": proxyType,
                "proxyAddress": proxyAddress,
                "proxyPort": proxyPort,
            }
            if proxyLogin and proxyPassword:
                task_data["proxyLogin"] = proxyLogin
                task_data["proxyPassword"] = proxyPassword

            self.create_task_payload["task"].update(task_data)

    def captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        steps: Optional[list[int]] = None,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Sync solving method

        Args:
            captcha_link: Captcha image URL (VKCaptchaImageTask)
            captcha_file: Captcha image file path (VKCaptchaImageTask)
            captcha_base64: Captcha image BASE64 info (VKCaptchaImageTask)
            steps: List of step values for VKCaptchaImageTask
            kwargs: additional params for `requests` library

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        if self.method == VKCaptchaEnm.VKCaptchaImageTask:
            self._body_file_processing(
                save_format=self.save_format,
                file_path=self.img_path,
                image_key="image",
                captcha_link=captcha_link,
                captcha_file=captcha_file,
                captcha_base64=captcha_base64,
            )
            if steps:
                self.create_task_payload["task"]["steps"] = steps
            if not self.result.errorId:
                return self._processing_response(**kwargs)
            return self.result.to_dict()

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        steps: Optional[list[int]] = None,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Async solving method

        Args:
            captcha_link: Captcha image URL (VKCaptchaImageTask)
            captcha_file: Captcha image file path (VKCaptchaImageTask)
            captcha_base64: Captcha image BASE64 info (VKCaptchaImageTask)
            steps: List of step values for VKCaptchaImageTask
            kwargs: additional params for `aiohttp` library

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        if self.method == VKCaptchaEnm.VKCaptchaImageTask:
            await self._aio_body_file_processing(
                save_format=self.save_format,
                file_path=self.img_path,
                image_key="image",
                captcha_link=captcha_link,
                captcha_file=captcha_file,
                captcha_base64=captcha_base64,
            )
            if steps:
                self.create_task_payload["task"]["steps"] = steps
            if not self.result.errorId:
                return await self._aio_processing_response()
            return self.result.to_dict()

        return await self._aio_processing_response()
