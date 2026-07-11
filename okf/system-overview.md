---
type: System Architecture
title: Python-rucaptcha system overview
description: A Python SDK that adapts CAPTCHA-solving tasks to several external provider APIs.
tags: [architecture, sdk, captcha]
source_paths:
  - README.md
  - ARCHITECTURE.md
  - pyproject.toml
confidence: observed
---

# Python-rucaptcha system overview

`python-rucaptcha` is a Python 3.9+ library for submitting CAPTCHA-solving tasks to RuCaptcha, 2Captcha, DeathByCaptcha, and CaptchaAI services [1]. It is a source-layout setuptools package rather than a server, worker, or command-line application [2].

## Domain model

The repository has two client paths:

1. **Standard solver adapters** expose one concrete class per CAPTCHA or control operation and delegate common transport behavior to [standard solver adapters](/standard-solver-adapters.md).
2. **CaptchaAI native client** submits provider-native classic multipart methods using packaged metadata; it intentionally does not follow the standard `BaseCaptcha` inheritance path [3]. See [CaptchaAI native client](/captchaai-native-client.md).

The shared foundation owns task serialization, service endpoint selection, HTTP sessions, polling, retries, and normalized response mappings [4]. The package keeps task state in memory and communicates with external services over HTTP; no internal database or long-running service runtime is defined by the source layout [2].

## Boundaries

```text
Library caller
  ├── standard solver adapter ──> shared task engine ──> provider task API
  └── CaptchaAI client ────────> native multipart transport ──> CaptchaAI API
```

CAPTCHA-specific fields and method validation belong to leaf modules, while shared transport and polling remain in `core/` [5]. Sync and async handlers preserve the same task meaning and result shape while using different I/O paths [4].

## Relationships

* The adapter boundary is detailed in [Standard solver adapters](/standard-solver-adapters.md).
* The end-to-end execution path is described in [Request lifecycle](/request-lifecycle.md).
* Wire-level models and provider selection are described in [Service contracts](/service-contracts.md).
* Build and documentation boundaries are described in [Packaging and documentation](/packaging-and-documentation.md).

# Citations

[1] `README.md` — States the supported Python version, providers, and library purpose.
[2] `ARCHITECTURE.md` and `pyproject.toml` — Describe the SDK/package boundary and source-layout packaging.
[3] `src/python_rucaptcha/captchaai.py` and `src/python_rucaptcha/core/captchaai.py` — Implement the separate native CaptchaAI façade and transport.
[4] `src/python_rucaptcha/core/base.py` and `src/python_rucaptcha/core/result_handler.py` — Implement shared sync/async processing and result polling.
[5] `src/python_rucaptcha/AGENTS.md` and `src/python_rucaptcha/core/AGENTS.md` — Define the leaf/core ownership boundary.
