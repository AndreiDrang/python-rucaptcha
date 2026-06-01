import shutil
from typing import Any, Union, Optional

from .core.base import BaseCaptcha
from .core.enums import (
    SaveFormatsEnm,
    CoordinatesCaptchaEnm,
    YandexSmartCaptchaEnm,
)


class YandexSmartCaptcha(BaseCaptcha):
    """
    The class is used to work with Yandex SmartCaptcha.

    Supports three 2Captcha task types:
      - YandexSmartCaptchaTaskProxyless (token, no proxy)
      - YandexSmartCaptchaTask          (token, user proxy)
      - CoordinatesTask                 (image, two imgType modes: smart_captcha, pazl_smart_captcha)

    Args:
        rucaptcha_key: User API key
        websiteURL: Full URL of the page where the captcha is loaded (token methods)
        websiteKey: Sitekey from the page source (token methods)
        method: Captcha type. Default YandexSmartCaptchaTaskProxyless.
        userAgent: Browser User-Agent to use (token methods, optional)
        cookies: Cookies to send in the request (token methods, optional, format "name1=value1;name2=value2")
        proxyType: Proxy type (http, https, socks4, socks5) - required for YandexSmartCaptchaTask
        proxyAddress: Proxy IP/hostname - required for YandexSmartCaptchaTask
        proxyPort: Proxy port - required for YandexSmartCaptchaTask
        proxyLogin: Proxy login (optional)
        proxyPassword: Proxy password (optional)
        imgType: Image variant type - "smart_captcha" or "pazl_smart_captcha" (CoordinatesTask only)
        comment: Text hint for the worker - required for imgType="smart_captcha"
        save_format: How to save the image - "temp" or "const" (CoordinatesTask only)
        img_clearing: Whether to delete the image folder on instance destruction
        img_path: Folder name for saved images

    Examples:
        >>> YandexSmartCaptcha(
        ...     rucaptcha_key="aa9011f31111181111168611f1151122",
        ...     websiteURL="https://example.com/",
        ...     websiteKey="Y5Lh0ti...",
        ... ).captcha_handler()
        {"errorId": 0, "status": "ready", "solution": {"token": "..."}, "taskId": ...}

        >>> await YandexSmartCaptcha(
        ...     rucaptcha_key="aa9011f31111181111168611f1151122",
        ...     websiteURL="https://example.com/",
        ...     websiteKey="Y5Lh0ti...",
        ...     method=YandexSmartCaptchaEnm.YandexSmartCaptchaTask,
        ...     proxyType="http",
        ...     proxyAddress="1.2.3.4",
        ...     proxyPort=8080,
        ... ).aio_captcha_handler()
        {"errorId": 0, "status": "ready", "solution": {"token": "..."}, "taskId": ...}

        >>> YandexSmartCaptcha(
        ...     rucaptcha_key="aa9011f31111181111168611f1151122",
        ...     method=CoordinatesCaptchaEnm.CoordinatesTask,
        ...     imgType="smart_captcha",
        ...     comment="select objects in the order of the instruction",
        ... ).captcha_handler(
        ...     captcha_file="src/examples/088636.png",
        ...     imgInstructions_file="src/examples/bounding_box_start.png",
        ... )
        {"errorId": 0, "status": "ready", "solution": {"coordinates": [{"x": 57, "y": 82}, ...]}, "taskId": ...}

    Notes:
        https://2captcha.com/api-docs/yandex-smart-captcha

        https://rucaptcha.com/api-docs/yandex-smart-captcha
    """

    _VALID_METHODS = YandexSmartCaptchaEnm.list_values() + [CoordinatesCaptchaEnm.CoordinatesTask.value]

    def __init__(
        self,
        websiteURL: Optional[str] = None,
        websiteKey: Optional[str] = None,
        method: Union[str, YandexSmartCaptchaEnm, CoordinatesCaptchaEnm] = (
            YandexSmartCaptchaEnm.YandexSmartCaptchaTaskProxyless
        ),
        userAgent: Optional[str] = None,
        cookies: Optional[str] = None,
        proxyType: Optional[str] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        imgType: Optional[str] = None,
        comment: Optional[str] = None,
        save_format: Union[str, SaveFormatsEnm] = SaveFormatsEnm.TEMP,
        img_clearing: bool = True,
        img_path: str = "PythonRuCaptchaYandexSmart",
        *args,
        **kwargs,
    ):
        method_str = method.value if hasattr(method, "value") else method

        if method_str not in self._VALID_METHODS:
            raise ValueError(f"Invalid method parameter set, available - {self._VALID_METHODS}")

        is_token = method_str in YandexSmartCaptchaEnm.list_values()
        is_image = method_str == CoordinatesCaptchaEnm.CoordinatesTask.value

        # token-method-specific validation
        if is_token:
            if not (websiteURL and websiteKey):
                raise ValueError(
                    "websiteURL and websiteKey are required for token methods "
                    f"({YandexSmartCaptchaEnm.list_values()})"
                )

        # proxy-method-specific validation
        if method_str == YandexSmartCaptchaEnm.YandexSmartCaptchaTask.value:
            if not all([proxyType, proxyAddress, proxyPort]):
                raise ValueError(
                    "proxyType, proxyAddress, and proxyPort are required for YandexSmartCaptchaTask"
                )

        # image-method-specific validation
        if is_image:
            if not imgType:
                raise ValueError("imgType is required for CoordinatesTask")
            if imgType == "smart_captcha" and not comment:
                raise ValueError('comment is required for CoordinatesTask with imgType="smart_captcha"')

        # Build task payload
        task_data: dict[str, Any] = {}
        if is_token:
            task_data["websiteURL"] = websiteURL
            task_data["websiteKey"] = websiteKey
            if userAgent is not None:
                task_data["userAgent"] = userAgent
            if cookies is not None:
                task_data["cookies"] = cookies
            if method_str == YandexSmartCaptchaEnm.YandexSmartCaptchaTask.value:
                task_data["proxyType"] = proxyType
                task_data["proxyAddress"] = proxyAddress
                task_data["proxyPort"] = proxyPort
                if proxyLogin is not None:
                    task_data["proxyLogin"] = proxyLogin
                if proxyPassword is not None:
                    task_data["proxyPassword"] = proxyPassword
        elif is_image:
            task_data["imgType"] = imgType
            if comment is not None:
                task_data["comment"] = comment

        super().__init__(method=method, *args, **kwargs)
        self.method = method_str
        self.save_format = save_format
        self.img_clearing = img_clearing
        self.img_path = img_path
        self.create_task_payload["task"].update(task_data)

    def captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        imgInstructions_link: Optional[str] = None,
        imgInstructions_file: Optional[str] = None,
        imgInstructions_base64: Optional[bytes] = None,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Sync solving method.
        """
        if self.method == CoordinatesCaptchaEnm.CoordinatesTask.value:
            self._body_file_processing(
                save_format=self.save_format,
                file_path=self.img_path,
                image_key="body",
                captcha_link=captcha_link,
                captcha_file=captcha_file,
                captcha_base64=captcha_base64,
                **kwargs,
            )
            if any([imgInstructions_link, imgInstructions_file, imgInstructions_base64]):
                self._body_file_processing(
                    save_format=self.save_format,
                    file_path=self.img_path,
                    image_key="imgInstructions",
                    captcha_link=imgInstructions_link,
                    captcha_file=imgInstructions_file,
                    captcha_base64=imgInstructions_base64,
                    **kwargs,
                )
            if not self.result.errorId:
                return self._processing_response(**kwargs)
            return self.result.to_dict()

        return self._processing_response(**kwargs)

    async def aio_captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        imgInstructions_link: Optional[str] = None,
        imgInstructions_file: Optional[str] = None,
        imgInstructions_base64: Optional[bytes] = None,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Async solving method.
        """
        if self.method == CoordinatesCaptchaEnm.CoordinatesTask.value:
            await self._aio_body_file_processing(
                save_format=self.save_format,
                file_path=self.img_path,
                image_key="body",
                captcha_link=captcha_link,
                captcha_file=captcha_file,
                captcha_base64=captcha_base64,
                **kwargs,
            )
            if any([imgInstructions_link, imgInstructions_file, imgInstructions_base64]):
                await self._aio_body_file_processing(
                    save_format=self.save_format,
                    file_path=self.img_path,
                    image_key="imgInstructions",
                    captcha_link=imgInstructions_link,
                    captcha_file=imgInstructions_file,
                    captcha_base64=imgInstructions_base64,
                    **kwargs,
                )
            if not self.result.errorId:
                return await self._aio_processing_response()
            return self.result.to_dict()

        return await self._aio_processing_response()

    def __del__(self):
        if (
            hasattr(self, "save_format")
            and self.save_format == SaveFormatsEnm.CONST.value
            and hasattr(self, "img_clearing")
            and self.img_clearing
        ):
            try:
                shutil.rmtree(self.img_path)
            except OSError:
                pass
