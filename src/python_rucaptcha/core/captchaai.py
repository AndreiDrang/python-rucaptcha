"""Transport CaptchaAI classic multipart requests using packaged metadata.

Provider contracts are data-driven, so native callers can submit documented
methods and future methods without adding task-type branches here.
"""

from __future__ import annotations

import json
import time
import asyncio
import logging
from typing import Any, Mapping
from pathlib import Path
from functools import lru_cache
from dataclasses import dataclass

import aiohttp
import requests

from .config import attempts_generator
from .serializer import GetTaskResultResponseSer

REQUEST_TIMEOUT = 30
_PENDING = "CAPCHA_NOT_READY"
_RESERVED_FIELDS = {"key", "method", "json"}


@dataclass(frozen=True)
class CaptchaAIFile:
    """Describe one binary part in a native CaptchaAI multipart request.

    Attributes:
        content: Bytes sent as the multipart field body.
        filename: Filename presented to the provider.
        content_type: MIME type presented for the file part.
    """

    content: bytes
    filename: str = "captcha.bin"
    content_type: str = "application/octet-stream"


@lru_cache(maxsize=1)
def _metadata() -> dict[str, Any]:
    """Load the packaged native CaptchaAI profile metadata once.

    Returns:
        Parsed profile and control-operation metadata.
    """
    data_path = Path(__file__).with_name("data") / "captchaai_profiles.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _legacy_metadata() -> dict[str, Any]:
    """Load the packaged legacy task translation metadata once.

    Returns:
        Parsed mappings from library task names to CaptchaAI profiles.
    """
    data_path = Path(__file__).with_name("data") / "captchaai_legacy_profiles.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


def profiles() -> tuple[str, ...]:
    """Return the packaged CaptchaAI profile names.

    Returns:
        Profile names available for declarative validation.
    """
    return tuple(_metadata()["profiles"])


def profile_method(profile_name: str) -> str:
    """Return the native method configured by a packaged profile.

    Args:
        profile_name: Name of the packaged profile to inspect.

    Returns:
        Provider-native method name for the profile.

    Raises:
        ValueError: If ``profile_name`` is not packaged.
    """
    return str(_profile(profile_name)["method"])


def _err(request: Any) -> dict[str, Any]:
    """Normalize a transport or provider failure into a result mapping.

    Args:
        request: Error value or provider error text to expose in the result.

    Returns:
        A failed ``GetTaskResultResponseSer`` mapping.
    """
    message = str(request) if request is not None else "ERROR_UNKNOWN"
    return GetTaskResultResponseSer(
        status="failed",
        errorId=12,
        errorCode=message,
        errorDescription=f"CaptchaAI returned: {message}",
    ).to_dict()


def _profile(profile_name: str | None) -> dict[str, Any]:
    """Resolve an optional packaged profile.

    Args:
        profile_name: Profile name, or ``None`` for unprofiled native calls.

    Returns:
        Profile metadata, or an empty mapping when no profile is selected.

    Raises:
        ValueError: If the requested profile is not packaged.
    """
    if profile_name is None:
        return {}
    try:
        return _metadata()["profiles"][profile_name]
    except KeyError as error:
        raise ValueError(f"Unknown CaptchaAI profile {profile_name!r}") from error


def _prepare_params(
    method: str,
    params: Mapping[str, Any] | None,
    files: Mapping[str, CaptchaAIFile] | None,
    profile_name: str | None,
) -> tuple[str, dict[str, Any], dict[str, CaptchaAIFile], dict[str, Any]]:
    """Apply profile defaults and validate a native method request.

    Args:
        method: Provider-native method name.
        params: Scalar provider parameters.
        files: Binary multipart fields.
        profile_name: Optional packaged profile used for validation.

    Returns:
        The method, prepared scalar parameters, file parts, and profile data.

    Raises:
        ValueError: If the request violates reserved-field, profile, or file
            validation rules.
    """
    if not method:
        raise ValueError("CaptchaAI method is required")
    profile = _profile(profile_name)
    supplied = dict(params or {})
    if invalid := _RESERVED_FIELDS.intersection(supplied):
        raise ValueError(f"CaptchaAI params cannot override reserved fields: {sorted(invalid)}")

    prepared_files = dict(files or {})
    for field, value in prepared_files.items():
        if not isinstance(value, CaptchaAIFile):
            raise ValueError(f"CaptchaAI file field {field!r} must be a CaptchaAIFile")

    prepared = {**profile.get("defaults", {}), **supplied}
    expected_method = profile.get("method")
    if expected_method is not None and method != expected_method:
        raise ValueError(f"Profile {profile_name!r} requires method {expected_method!r}")

    file_fields = set(profile.get("file_fields", []))
    missing = [
        field
        for field in profile.get("required", [])
        if (field not in prepared_files if field in file_fields else field not in prepared)
    ]
    if missing:
        raise ValueError(
            f"CaptchaAI profile {profile_name!r} is missing required fields: {', '.join(missing)}"
        )

    unexpected_files = set(prepared_files).difference(file_fields) if file_fields else set()
    if unexpected_files and profile_name is not None:
        raise ValueError(
            f"CaptchaAI profile {profile_name!r} does not accept files: {sorted(unexpected_files)}"
        )
    return method, prepared, prepared_files, profile


def _proxy_params(task: Mapping[str, Any]) -> dict[str, str]:
    """Translate canonical proxy fields to CaptchaAI classic API fields.

    Args:
        task: Legacy library task containing canonical proxy fields.

    Returns:
        Provider-native ``proxy`` and ``proxytype`` fields, or an empty mapping
        when no proxy fields are present.

    Raises:
        ValueError: If required proxy fields are incomplete or invalid.
    """
    fields = ("proxyType", "proxyAddress", "proxyPort", "proxyLogin", "proxyPassword")
    if not any(task.get(field) is not None for field in fields):
        return {}

    proxy_type = task.get("proxyType")
    proxy_address = task.get("proxyAddress")
    proxy_port = task.get("proxyPort")
    if not all((proxy_type, proxy_address, proxy_port)):
        raise ValueError("proxyType, proxyAddress, and proxyPort must be supplied together")

    normalized_type = str(proxy_type).upper()
    if normalized_type not in {"HTTP", "HTTPS", "SOCKS4", "SOCKS5"}:
        raise ValueError("proxyType must be HTTP, HTTPS, SOCKS4, or SOCKS5")

    proxy_login = task.get("proxyLogin")
    proxy_password = task.get("proxyPassword")
    if (proxy_login is None) != (proxy_password is None):
        raise ValueError("proxyLogin and proxyPassword must be supplied together")

    proxy = f"{proxy_address}:{proxy_port}"
    if proxy_login is not None:
        proxy = f"{proxy_login}:{proxy_password}@{proxy}"
    return {"proxy": proxy, "proxytype": normalized_type}


def _legacy_request(task: Mapping[str, Any]) -> tuple[str, dict[str, Any], str | None]:
    """Translate a legacy task through packaged compatibility metadata.

    Args:
        task: Existing library task payload.

    Returns:
        Provider method, provider-native parameters, and optional profile name.

    Raises:
        ValueError: If no compatibility profile exists or explicit parameters
            are not a mapping.
    """
    explicit_method = task.get("captchaai_method")
    explicit_profile = task.get("captchaai_profile")
    if explicit_method is not None:
        explicit_params = task.get("captchaai_params", {})
        if not isinstance(explicit_params, Mapping):
            raise ValueError("captchaai_params must be a mapping")
        return str(explicit_method), dict(explicit_params), explicit_profile

    task_type = getattr(task.get("type"), "value", task.get("type"))
    task_config = _legacy_metadata().get(str(task_type))
    if task_config is None:
        raise ValueError(
            "No CaptchaAI compatibility profile exists for this library task. "
            "Use the native CaptchaAI client with method and params."
        )

    params: dict[str, Any] = {}
    bool_int = set(task_config.get("bool_int", []))
    for source, target in task_config.get("fields", {}).items():
        if task.get(source) is not None:
            value = task[source]
            params[target] = int(bool(value)) if source in bool_int else value
    if task_config.get("proxy"):
        params.update(_proxy_params(task))

    profile_name = task_config["profile"]
    method = _profile(profile_name)["method"]
    return method, params, profile_name


def _requests_form(
    fields: Mapping[str, Any], files: Mapping[str, CaptchaAIFile]
) -> dict[str, tuple[Any, ...]]:
    """Build requests-compatible multipart parts.

    Args:
        fields: Scalar fields to encode as text parts.
        files: Binary fields to encode with filename and MIME metadata.

    Returns:
        Multipart parts accepted by ``requests.Session.post``.
    """
    form: dict[str, tuple[Any, ...]] = {name: (None, str(value)) for name, value in fields.items()}
    for name, value in files.items():
        form[name] = (value.filename, value.content, value.content_type)
    return form


def _aio_form(fields: Mapping[str, Any], files: Mapping[str, CaptchaAIFile]) -> aiohttp.FormData:
    """Build an aiohttp multipart form from scalar and binary fields.

    Args:
        fields: Scalar fields to encode as text parts.
        files: Binary fields to encode with filename and MIME metadata.

    Returns:
        Multipart form suitable for an aiohttp POST request.
    """
    form = aiohttp.FormData()
    for name, value in fields.items():
        form.add_field(name, str(value), content_type="text/plain")
    for name, value in files.items():
        form.add_field(name, value.content, filename=value.filename, content_type=value.content_type)
    return form


def _response_payload(response: Any) -> dict[str, Any]:
    """Validate the JSON response shape expected by the transport.

    Args:
        response: Decoded provider response.

    Returns:
        The response as a dictionary.

    Raises:
        ValueError: If the response is not a JSON object.
    """
    if not isinstance(response, dict):
        raise ValueError("response is not a JSON object")
    return response


def _error_value(response: Mapping[str, Any]) -> Any:
    """Select the most useful provider error value from a response.

    Args:
        response: Provider response mapping.

    Returns:
        The first available provider error value, or ``ERROR_UNKNOWN``.
    """
    return (
        response.get("request")
        or response.get("error")
        or response.get("errorDescription")
        or "ERROR_UNKNOWN"
    )


def _ready(task_id: str | None, response: Mapping[str, Any], profile: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize a successful provider response and apply profile aliases.

    Args:
        task_id: Provider task identifier, if the request was polled.
        response: Successful provider response mapping.
        profile: Profile metadata containing optional result aliases.

    Returns:
        A ready ``GetTaskResultResponseSer`` mapping.
    """
    solution = {key: value for key, value in response.items() if key != "status"}
    for alias, source in profile.get("aliases", {}).items():
        if source in solution:
            value = solution[source]
            if alias == "click" and isinstance(value, str):
                try:
                    value = json.loads(value)
                except ValueError:
                    pass
            solution[alias] = value
    return GetTaskResultResponseSer(status="ready", solution=solution, taskId=task_id).to_dict()


def _is_success(response: Mapping[str, Any], profile: Mapping[str, Any]) -> bool:
    """Determine whether a response satisfies its profile success contract.

    Args:
        response: Provider response mapping.
        profile: Profile metadata containing optional success fields.

    Returns:
        ``True`` when the standard status or all profile success fields match.
    """
    if response.get("status") == 1:
        return True
    success_fields = profile.get("success_fields", [])
    return bool(success_fields) and all(field in response for field in success_fields)


def _submit_url(url_request: str, profile: Mapping[str, Any]) -> str:
    """Resolve a profile-specific submission URL from the configured base URL.

    Args:
        url_request: Configured default submission URL.
        profile: Profile metadata containing an optional submission path.

    Returns:
        Submission URL selected for the profile.
    """
    path = profile.get("submit_path", "/in.php")
    if path == "/in.php":
        return url_request
    return f"{url_request.rsplit('/', 1)[0]}{path}"


def solve_native(
    key: str,
    method: str,
    params: Mapping[str, Any] | None,
    url_request: str,
    url_response: str,
    sleep_time: int,
    *,
    files: Mapping[str, CaptchaAIFile] | None = None,
    profile: str | None = None,
    poll: bool | None = None,
    session: requests.Session | None = None,
) -> dict[str, Any]:
    """Submit and optionally poll any CaptchaAI classic API method.

    Args:
        key: CaptchaAI API key.
        method: Provider-native method name.
        params: Scalar provider parameters.
        url_request: Submission URL.
        url_response: Polling URL.
        sleep_time: Seconds between polling attempts.
        files: Optional binary multipart fields.
        profile: Optional packaged profile name.
        poll: Whether to poll after submission.
        session: Optional requests session to reuse.

    Returns:
        A normalized ready or failed result mapping.
    """
    try:
        method, params, files, profile_data = _prepare_params(method, params, files, profile)
    except ValueError as error:
        return _err(error)

    should_poll = profile_data.get("poll", True) if poll is None else poll
    data = {"key": key, "method": method, "json": 1, **params}
    http = session or requests.Session()
    try:
        response = http.post(
            _submit_url(url_request, profile_data),
            files=_requests_form(data, files),
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        created = _response_payload(response.json())
    except (requests.RequestException, ValueError) as error:
        return _err(f"ERROR_SUBMIT {error}")

    if not should_poll:
        if _is_success(created, profile_data):
            return _ready(None, created, profile_data)
        return _err(_error_value(created))
    if created.get("status") != 1 or not isinstance(created.get("request"), str):
        return _err(_error_value(created))

    task_id = created["request"]
    time.sleep(sleep_time)
    for _ in attempts_generator():
        try:
            response = http.post(
                url_response,
                files=_requests_form({"key": key, "action": "get", "id": task_id, "json": 1}, {}),
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            result = _response_payload(response.json())
        except (requests.RequestException, ValueError) as error:
            return _err(f"ERROR_POLL {error}")
        logging.info("CaptchaAI sync result received for task %s", task_id)
        if result.get("request") == _PENDING:
            time.sleep(sleep_time)
            continue
        if _is_success(result, profile_data):
            return _ready(task_id, result, profile_data)
        return _err(_error_value(result))
    return _err("ERROR_TIMEOUT")


async def aio_solve_native(
    key: str,
    method: str,
    params: Mapping[str, Any] | None,
    url_request: str,
    url_response: str,
    sleep_time: int,
    *,
    files: Mapping[str, CaptchaAIFile] | None = None,
    profile: str | None = None,
    poll: bool | None = None,
) -> dict[str, Any]:
    """Asynchronously submit and optionally poll a CaptchaAI method.

    Args:
        key: CaptchaAI API key.
        method: Provider-native method name.
        params: Scalar provider parameters.
        url_request: Submission URL.
        url_response: Polling URL.
        sleep_time: Seconds between polling attempts.
        files: Optional binary multipart fields.
        profile: Optional packaged profile name.
        poll: Whether to poll after submission.

    Returns:
        A normalized ready or failed result mapping.
    """
    try:
        method, params, files, profile_data = _prepare_params(method, params, files, profile)
    except ValueError as error:
        return _err(error)

    should_poll = profile_data.get("poll", True) if poll is None else poll
    data = {"key": key, "method": method, "json": 1, **params}
    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as http:
        try:
            async with http.post(
                _submit_url(url_request, profile_data), data=_aio_form(data, files)
            ) as response:
                response.raise_for_status()
                created = _response_payload(await response.json(content_type=None))
        except (aiohttp.ClientError, ValueError) as error:
            return _err(f"ERROR_SUBMIT {error}")

        if not should_poll:
            if _is_success(created, profile_data):
                return _ready(None, created, profile_data)
            return _err(_error_value(created))
        if created.get("status") != 1 or not isinstance(created.get("request"), str):
            return _err(_error_value(created))

        task_id = created["request"]
        await asyncio.sleep(sleep_time)
        for _ in attempts_generator():
            try:
                poll_data = {"key": key, "action": "get", "id": task_id, "json": 1}
                async with http.post(url_response, data=_aio_form(poll_data, {})) as response:
                    response.raise_for_status()
                    result = _response_payload(await response.json(content_type=None))
            except (aiohttp.ClientError, ValueError) as error:
                return _err(f"ERROR_POLL {error}")
            logging.info("CaptchaAI async result received for task %s", task_id)
            if result.get("request") == _PENDING:
                await asyncio.sleep(sleep_time)
                continue
            if _is_success(result, profile_data):
                return _ready(task_id, result, profile_data)
            return _err(_error_value(result))
    return _err("ERROR_TIMEOUT")


def solve(
    create_task_payload: Mapping[str, Any],
    url_request: str,
    url_response: str,
    sleep_time: int,
    session: requests.Session | None = None,
) -> dict[str, Any]:
    """Solve a legacy library task through CaptchaAI compatibility metadata.

    Args:
        create_task_payload: Existing library create-task payload.
        url_request: CaptchaAI submission URL.
        url_response: CaptchaAI polling URL.
        sleep_time: Seconds between polling attempts.
        session: Optional requests session to reuse.

    Returns:
        A normalized ready or failed result mapping.
    """
    try:
        method, params, profile = _legacy_request(create_task_payload["task"])
    except (KeyError, ValueError) as error:
        return _err(error)
    return solve_native(
        key=str(create_task_payload["clientKey"]),
        method=method,
        params=params,
        profile=profile,
        url_request=url_request,
        url_response=url_response,
        sleep_time=sleep_time,
        session=session,
    )


async def aio_solve(
    create_task_payload: Mapping[str, Any],
    url_request: str,
    url_response: str,
    sleep_time: int,
) -> dict[str, Any]:
    """Asynchronously solve a legacy task through compatibility metadata.

    Args:
        create_task_payload: Existing library create-task payload.
        url_request: CaptchaAI submission URL.
        url_response: CaptchaAI polling URL.
        sleep_time: Seconds between polling attempts.

    Returns:
        A normalized ready or failed result mapping.
    """
    try:
        method, params, profile = _legacy_request(create_task_payload["task"])
    except (KeyError, ValueError) as error:
        return _err(error)
    return await aio_solve_native(
        key=str(create_task_payload["clientKey"]),
        method=method,
        params=params,
        profile=profile,
        url_request=url_request,
        url_response=url_response,
        sleep_time=sleep_time,
    )


def control(
    key: str,
    name: str,
    url_response: str,
    session: requests.Session | None = None,
) -> dict[str, Any]:
    """Execute a declarative CaptchaAI control operation.

    Args:
        key: CaptchaAI API key.
        name: Packaged control-operation name.
        url_response: CaptchaAI control endpoint.
        session: Optional requests session to reuse.

    Returns:
        The provider control response or a normalized failed result.
    """
    try:
        control_data = _metadata()["controls"][name]
    except KeyError:
        return _err(f"Unknown CaptchaAI control operation {name!r}")

    try:
        response = (session or requests.Session()).post(
            url_response,
            files=_requests_form({"key": key, "json": 1, "action": control_data["action"]}, {}),
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        payload = _response_payload(response.json())
    except (requests.RequestException, ValueError) as error:
        return _err(f"ERROR_CONTROL {error}")

    if payload.get("status") == 0:
        return _err(_error_value(payload))
    result = {field: value for field, value in payload.items() if field != "status"}
    for alias, source in control_data.get("aliases", {}).items():
        if source in result:
            result[alias] = result[source]
    return result


async def aio_control(key: str, name: str, url_response: str) -> dict[str, Any]:
    """Asynchronously execute a declarative CaptchaAI control operation.

    Args:
        key: CaptchaAI API key.
        name: Packaged control-operation name.
        url_response: CaptchaAI control endpoint.

    Returns:
        The provider control response or a normalized failed result.
    """
    try:
        control_data = _metadata()["controls"][name]
    except KeyError:
        return _err(f"Unknown CaptchaAI control operation {name!r}")

    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as http:
            data = {"key": key, "json": 1, "action": control_data["action"]}
            async with http.post(url_response, data=_aio_form(data, {})) as response:
                response.raise_for_status()
                payload = _response_payload(await response.json(content_type=None))
    except (aiohttp.ClientError, ValueError) as error:
        return _err(f"ERROR_CONTROL {error}")

    if payload.get("status") == 0:
        return _err(_error_value(payload))
    result = {field: value for field, value in payload.items() if field != "status"}
    for alias, source in control_data.get("aliases", {}).items():
        if source in result:
            result[alias] = result[source]
    return result
