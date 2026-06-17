"""
CaptchaAI provider adapter.

CaptchaAI (https://captchaai.com) is 2Captcha-API-compatible but exposes the
**classic** ``in.php`` / ``res.php`` form-parameter API rather than the newer
JSON ``createTask`` / ``getTaskResult`` API the rest of this library speaks.

This module translates the library's internal ``create_task_payload`` (the v2
JSON task dict) into the classic form parameters CaptchaAI expects, submits the
task, polls for the result, and returns a response shaped like
``GetTaskResultResponseSer.to_dict()`` so the public ``Turnstile`` / ``ReCaptcha``
/ ``ImageCaptcha`` classes work transparently when ``service_type`` is
``ServiceEnm.CAPTCHAAI``.

Supported task types (the ones CaptchaAI solves through the classic API):
``TurnstileTaskProxyless``/``TurnstileTask``, ``RecaptchaV2TaskProxyless``/
``RecaptchaV2Task``, ``RecaptchaV3TaskProxyless``, ``ImageToTextTask``.
Other task types raise a clear ``ValueError`` so callers fail fast rather than
silently sending an unsupported method.
"""

from __future__ import annotations

import time
import asyncio
import logging
from typing import Any

import aiohttp
import requests

from .config import attempts_generator
from .serializer import GetTaskResultResponseSer

# v2 task ``type`` -> classic ``method``
_TURNSTILE = {"TurnstileTaskProxyless", "TurnstileTask"}
_RECAPTCHA_V2 = {
    "RecaptchaV2TaskProxyless",
    "RecaptchaV2Task",
    "RecaptchaV2EnterpriseTaskProxyless",
    "RecaptchaV2EnterpriseTask",
}
_RECAPTCHA_V3 = {"RecaptchaV3TaskProxyless"}
_IMAGE = {"ImageToTextTask"}


def _err(request: str | None) -> dict[str, Any]:
    return GetTaskResultResponseSer(
        status="failed",
        errorId=12,
        errorCode=request or "ERROR_UNKNOWN",
        errorDescription=f"CaptchaAI returned: {request}",
    ).to_dict()


def build_classic_params(task: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Map a v2 task dict to (classic ``method``, classic params)."""
    ctype = task.get("type")
    extra: dict[str, Any] = {}

    if ctype in _TURNSTILE:
        method = "turnstile"
        extra["sitekey"] = task["websiteKey"]
        extra["pageurl"] = task["websiteURL"]
        if task.get("action"):
            extra["action"] = task["action"]
        if task.get("data"):
            extra["data"] = task["data"]
    elif ctype in _RECAPTCHA_V2:
        method = "userrecaptcha"
        extra["googlekey"] = task["websiteKey"]
        extra["pageurl"] = task["websiteURL"]
        if "Enterprise" in (ctype or ""):
            extra["enterprise"] = 1
    elif ctype in _RECAPTCHA_V3:
        method = "userrecaptcha"
        extra["googlekey"] = task["websiteKey"]
        extra["pageurl"] = task["websiteURL"]
        extra["version"] = "v3"
        if task.get("pageAction"):
            extra["action"] = task["pageAction"]
        if task.get("minScore"):
            extra["min_score"] = task["minScore"]
    elif ctype in _IMAGE:
        method = "base64"
        extra["body"] = task["body"]
    else:
        raise ValueError(
            f"CaptchaAI provider does not support task type {ctype!r}. "
            f"Supported: Turnstile, ReCaptchaV2, ReCaptchaV3, ImageToText."
        )

    # pass-through proxy / user-agent if present
    if task.get("userAgent"):
        extra["userAgent"] = task["userAgent"]
    return method, extra


def _solution(method: str, token: str) -> dict[str, str]:
    if method == "base64":
        return {"text": token}
    return {"token": token, "gRecaptchaResponse": token}


def solve(
    create_task_payload: dict[str, Any],
    url_request: str,
    url_response: str,
    sleep_time: int,
) -> dict[str, Any]:
    """Synchronous classic in.php/res.php solve."""
    key = create_task_payload["clientKey"]
    task = create_task_payload["task"]
    try:
        method, extra = build_classic_params(task)
    except (KeyError, ValueError) as error:
        return _err(str(error))

    data = {"key": key, "method": method, "json": 1, **extra}
    try:
        created = requests.post(url_request, data=data).json()
    except Exception as error:  # noqa: BLE001
        return _err(f"ERROR_SUBMIT {error}")
    if created.get("status") != 1:
        return _err(created.get("request"))

    captcha_id = created["request"]
    time.sleep(sleep_time)
    for _ in attempts_generator():
        try:
            res = requests.get(
                url_response,
                params={"key": key, "action": "get", "id": captcha_id, "json": 1},
            ).json()
            logging.info(f"CaptchaAI sync result - {res = }")
        except Exception as error:  # noqa: BLE001
            return _err(f"ERROR_POLL {error}")
        if res.get("status") == 1:
            return GetTaskResultResponseSer(
                status="ready",
                solution=_solution(method, res["request"]),
                taskId=captcha_id if str(captcha_id).isdigit() else None,
            ).to_dict()
        if res.get("request") == "CAPCHA_NOT_READY":
            time.sleep(sleep_time)
            continue
        return _err(res.get("request"))
    return _err("ERROR_TIMEOUT")


async def aio_solve(
    create_task_payload: dict[str, Any],
    url_request: str,
    url_response: str,
    sleep_time: int,
) -> dict[str, Any]:
    """Asynchronous classic in.php/res.php solve."""
    key = create_task_payload["clientKey"]
    task = create_task_payload["task"]
    try:
        method, extra = build_classic_params(task)
    except (KeyError, ValueError) as error:
        return _err(str(error))

    data = {"key": key, "method": method, "json": 1, **extra}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url_request, data=data) as resp:
                created = await resp.json(content_type=None)
        except Exception as error:  # noqa: BLE001
            return _err(f"ERROR_SUBMIT {error}")
        if created.get("status") != 1:
            return _err(created.get("request"))

        captcha_id = created["request"]
        await asyncio.sleep(sleep_time)
        for _ in attempts_generator():
            try:
                async with session.get(
                    url_response,
                    params={"key": key, "action": "get", "id": captcha_id, "json": 1},
                ) as resp:
                    res = await resp.json(content_type=None)
                    logging.info(f"CaptchaAI async result - {res = }")
            except Exception as error:  # noqa: BLE001
                return _err(f"ERROR_POLL {error}")
            if res.get("status") == 1:
                return GetTaskResultResponseSer(
                    status="ready",
                    solution=_solution(method, res["request"]),
                    taskId=captcha_id if str(captcha_id).isdigit() else None,
                ).to_dict()
            if res.get("request") == "CAPCHA_NOT_READY":
                await asyncio.sleep(sleep_time)
                continue
            return _err(res.get("request"))
    return _err("ERROR_TIMEOUT")
