---
type: API Contract
title: Provider and result contracts
description: Shared provider selection, task envelope, and normalized response vocabulary.
tags: [api, providers, serialization, enums]
source_paths:
  - src/python_rucaptcha/core/enums.py
  - src/python_rucaptcha/core/serializer.py
  - src/python_rucaptcha/core/base.py
confidence: observed
---

# Provider and result contracts

## Provider selection

`ServiceEnm` defines four supported service identifiers: `2captcha`, `rucaptcha`, `deathbycaptcha`, and `captchaai` [1]. `CaptchaOptionsSer.urls_set()` maps them to their wire endpoints:

* 2Captcha and RuCaptcha use `createTask` and `getTaskResult` JSON endpoints.
* DeathByCaptcha uses the compatible `2captcha/in.php` and `2captcha/res.php` paths.
* CaptchaAI uses `https://ocr.captchaai.com/in.php` and `/res.php` [2].

The base client normalizes enum values to strings before endpoint selection [2].

## Standard task envelope

The create request contains `clientKey` and a `task` object whose required discriminator is `type`; the serializer also defines `languagePool`, optional `callbackUrl`, and a package `soft_id` [2]. Concrete adapters add task-specific fields to this envelope [3].

## Normalized result

`GetTaskResultResponseSer` provides a common result shape with `status`, optional `solution`, cost and timing metadata, task ID, optional balance, and error fields (`errorId`, `errorCode`, and `errorDescription`) [2]. Both standard and native paths return dictionary representations of this model for success and most failures [3][4].

## Task vocabulary

The enum module contains service, save-format, control-operation, and CAPTCHA-specific method enums. The method values are the provider task names used in task payloads, such as `HCaptchaTaskProxyless`, `ImageToTextTask`, and `TurnstileTask` [1].

## Relationships

* The contract is consumed by the [request lifecycle](/request-lifecycle.md).
* Adapter-specific task semantics are described in [standard solver adapters](/standard-solver-adapters.md).
* CaptchaAI profile aliases extend the common result vocabulary in [CaptchaAI native client](/captchaai-native-client.md).

# Citations

[1] `src/python_rucaptcha/core/enums.py` — Defines service identifiers and task/control method values.
[2] `src/python_rucaptcha/core/serializer.py` — Defines endpoint selection, request envelopes, and normalized response fields.
[3] `src/python_rucaptcha/core/base.py` — Builds the standard task envelope and returns serialized results.
[4] `src/python_rucaptcha/core/captchaai.py` — Converts native success and error responses into the shared result model.
