"""Native, future-compatible CaptchaAI classic API client."""

from __future__ import annotations

from typing import Any, Mapping

import requests
from requests.adapters import HTTPAdapter

from .core import captchaai as transport
from .core.enums import ServiceEnm
from .core.config import RETRIES
from .core.serializer import CaptchaOptionsSer

CaptchaAIFile = transport.CaptchaAIFile


class CaptchaAI:
    """Client for CaptchaAI's classic multipart API.

    A packaged profile can validate a documented method contract. Omitting the
    profile allows provider-native parameters for methods not yet represented
    in the package metadata.

    Attributes:
        key: CaptchaAI API key used for requests.
        method: Provider method submitted by the client.
        params: Provider-native scalar parameters.
        files: Multipart file parts keyed by provider field name.
        profile: Optional packaged profile name.
        poll: Whether to poll for a result after submission.
    """

    def __init__(
        self,
        rucaptcha_key: str,
        method: str | None = None,
        params: Mapping[str, Any] | None = None,
        *,
        files: Mapping[str, CaptchaAIFile] | None = None,
        profile: str | None = None,
        poll: bool | None = None,
        sleep_time: int = 10,
    ):
        """Create a client for one CaptchaAI method.

        Args:
            rucaptcha_key: API key used for CaptchaAI requests.
            method: Provider-native method name. Required unless ``profile``
                supplies the method.
            params: Provider-native scalar parameters.
            files: Multipart file parts keyed by provider field name.
            profile: Optional packaged profile used for validation and defaults.
            poll: Whether to poll after submission. If omitted, the profile
                determines the default and native methods poll by default.
            sleep_time: Seconds between result polls.

        Raises:
            ValueError: If neither ``method`` nor ``profile`` is supplied.
        """
        if method is None:
            if profile is None:
                raise ValueError("CaptchaAI requires a method or a documented profile")
            method = transport.profile_method(profile)

        self.key = rucaptcha_key
        self.method = method
        self.params = dict(params or {})
        self.files = dict(files or {})
        self.profile = profile
        self.poll = poll
        self.options = CaptchaOptionsSer(sleep_time=sleep_time, service_type=ServiceEnm.CAPTCHAAI)
        self.options.urls_set()
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=RETRIES))
        self.session.mount("https://", HTTPAdapter(max_retries=RETRIES))

    @classmethod
    def profiles(cls) -> tuple[str, ...]:
        """List the packaged CaptchaAI profile names.

        Returns:
            Profile names available for declarative validation.
        """
        return transport.profiles()

    def captcha_handler(self) -> dict[str, Any]:
        """Submit the configured method and optionally poll for its result.

        Returns:
            A normalized result mapping containing either the solution or an
            error description.
        """
        return transport.solve_native(
            key=self.key,
            method=self.method,
            params=self.params,
            files=self.files,
            profile=self.profile,
            poll=self.poll,
            url_request=self.options.url_request,
            url_response=self.options.url_response,
            sleep_time=self.options.sleep_time,
            session=self.session,
        )

    async def aio_captcha_handler(self) -> dict[str, Any]:
        """Asynchronously submit the method and optionally poll for its result.

        Returns:
            A normalized result mapping containing either the solution or an
            error description.
        """
        return await transport.aio_solve_native(
            key=self.key,
            method=self.method,
            params=self.params,
            files=self.files,
            profile=self.profile,
            poll=self.poll,
            url_request=self.options.url_request,
            url_response=self.options.url_response,
            sleep_time=self.options.sleep_time,
        )

    def get_balance(self) -> dict[str, Any]:
        """Fetch the account balance through the CaptchaAI control API.

        Returns:
            The provider response with the balance value when successful, or
            the normalized error mapping returned by the transport.
        """
        return transport.control(self.key, "balance", self.options.url_response, session=self.session)

    async def aio_get_balance(self) -> dict[str, Any]:
        """Asynchronously fetch the account balance.

        Returns:
            The provider response with the balance value when successful, or
            the normalized error mapping returned by the transport.
        """
        return await transport.aio_control(self.key, "balance", self.options.url_response)

    def get_threads_info(self) -> dict[str, Any]:
        """Fetch total and active thread information.

        Returns:
            The provider response with thread information, or the normalized
            error mapping returned by the transport.
        """
        return transport.control(self.key, "threads_info", self.options.url_response, session=self.session)

    async def aio_get_threads_info(self) -> dict[str, Any]:
        """Asynchronously fetch total and active thread information.

        Returns:
            The provider response with thread information, or the normalized
            error mapping returned by the transport.
        """
        return await transport.aio_control(self.key, "threads_info", self.options.url_response)
