---
type: API Client
title: CaptchaAI native client
description: A data-driven client for CaptchaAI's classic multipart in.php/res.php protocol.
tags: [captchaai, multipart, profiles, compatibility]
source_paths:
  - src/python_rucaptcha/captchaai.py
  - src/python_rucaptcha/core/captchaai.py
  - src/python_rucaptcha/core/data/captchaai_profiles.json
  - src/python_rucaptcha/core/data/captchaai_legacy_profiles.json
  - pyproject.toml
confidence: observed
---

# CaptchaAI native client

`CaptchaAI` is a separate façade for CaptchaAI's classic multipart API. It accepts a provider-native `method`, scalar `params`, optional `CaptchaAIFile` parts, an optional packaged `profile`, and a polling preference [1]. It provides synchronous and asynchronous solving plus balance and thread-information controls [1].

## Profile-driven validation

The current native metadata defines 18 named profiles and two controls. Profiles provide method names, defaults, required scalar or file fields, optional submission paths, polling defaults, and response aliases [2]. For example, normal image profiles distinguish base64 and multipart-file inputs, while CAPTCHA profiles define required site fields and aliases such as `token`, `gRecaptchaResponse`, `cf_clearance`, or `click` [2].

When a profile is supplied, the transport validates the method, reserved fields, required inputs, file types, and accepted file fields. When no profile is supplied, provider-native parameters pass through after basic reserved-field validation [3].

## Submission and polling

The transport sends `key`, `method`, and `json=1` as multipart fields, optionally adds profile parameters and binary parts, and submits to `/in.php` or a profile-specific path [3]. If polling is enabled, it uses the provider task ID and repeatedly posts `action=get` to `/res.php` until the provider returns a solution, an error, or the bounded timeout path [3]. Native success and failure responses are normalized to the shared result model [3].

## Compatibility path

Legacy `BaseCaptcha` tasks can be translated through packaged compatibility metadata. The legacy mapping converts known task names and proxy fields into native method parameters; unsupported tasks return an explicit instruction to use the native client [3][4]. This keeps provider method expansion in data rather than per-method Python branches.

## Packaging requirement

Both profile JSON files are runtime inputs and are declared as package data in `pyproject.toml`; removing them from the wheel would break profile lookup and compatibility translation [3][5].

## Relationships

* Service URL selection is part of [provider and result contracts](/service-contracts.md).
* The native path is intentionally separate from [standard solver adapters](/standard-solver-adapters.md).
* Public examples are summarized in [public usage surface](/public-usage-surface.md).

# Citations

[1] `src/python_rucaptcha/captchaai.py` — Defines the native façade, file type, handlers, profiles, and controls.
[2] `src/python_rucaptcha/core/data/captchaai_profiles.json` — Defines the current native profiles, required fields, aliases, paths, and controls.
[3] `src/python_rucaptcha/core/captchaai.py` — Implements metadata validation, multipart submission, polling, normalization, and controls.
[4] `src/python_rucaptcha/core/data/captchaai_legacy_profiles.json` — Defines legacy task-to-profile compatibility mappings.
[5] `pyproject.toml` — Declares `core/data/*.json` as package data.
