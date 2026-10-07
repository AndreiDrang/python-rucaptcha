---
type: Architecture Component
title: Standard solver adapters
description: Flat CAPTCHA-specific modules that prepare task fields and delegate execution to BaseCaptcha.
tags: [captcha, adapters, sync, async]
source_paths:
  - src/python_rucaptcha/AGENTS.md
  - src/python_rucaptcha/hcaptcha.py
  - src/python_rucaptcha/image_captcha.py
  - src/python_rucaptcha/core/base.py
confidence: observed
---

# Standard solver adapters

A standard adapter is a concrete CAPTCHA class whose responsibility is to shape one provider task, validate its method choices, and expose synchronous and asynchronous handlers [1]. The modules are deliberately flat and use the existing `*_captcha.py` naming convention [1].

## Adapter responsibilities

* Call `BaseCaptcha` with the provider task type.
* Add CAPTCHA-specific fields to the task payload.
* Validate task methods against the corresponding enum where applicable.
* Keep sync and async handler entry points aligned.
* Leave HTTP submission, polling, retries, and common result handling to `core/` [1][2].

For example, `HCaptcha` sets `websiteURL` and `websiteKey`, validates the selected method against `HCaptchaEnm`, and routes both handlers to the shared processing methods [3]. `ImageCaptcha` adds input preparation for a URL, local file, or base64 bytes before invoking the same shared flow [4].

## Input handling

The base layer can encode local files and byte content as base64, fetch a source URL, and optionally save the fetched content to a configured directory [2][4]. The image adapter reports a normalized error instead of submitting when none of its accepted inputs is provided [4].

## Relationships

* Adapters depend on the [request lifecycle](/request-lifecycle.md) and [service contracts](/service-contracts.md).
* CaptchaAI is a deliberate exception documented in [CaptchaAI native client](/captchaai-native-client.md).
* New solver additions are expected to include a module, enum, tests, and documentation example [1].

# Citations

[1] `src/python_rucaptcha/AGENTS.md` — Defines module naming, adapter ownership, and addition requirements.
[2] `src/python_rucaptcha/core/base.py` — Implements the shared payload, session, file, and sync/async processing helpers.
[3] `src/python_rucaptcha/hcaptcha.py` — Shows task-field preparation, method validation, and paired handlers.
[4] `src/python_rucaptcha/image_captcha.py` — Shows URL/file/base64 input preparation and error gating before submission.
