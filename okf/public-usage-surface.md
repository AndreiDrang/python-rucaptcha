---
type: Public API Surface
title: Public usage surface
description: Repository-documented installation, solver usage, service selection, and native CaptchaAI entry points.
tags: [api, usage, documentation]
source_paths:
  - README.md
  - docs/index.rst
  - src/python_rucaptcha/__init__.py
  - src/python_rucaptcha/captchaai.py
confidence: observed
---

# Public usage surface

## Documented usage

The README presents installation with `pip install python-rucaptcha`, API-key-based solver construction, synchronous and asynchronous handlers, service switching through `ServiceEnm`, and examples for common CAPTCHA types [1]. It also documents native CaptchaAI calls with a profile or with provider-native fields [1].

The Sphinx root navigation publishes general modules, many CAPTCHA examples, CaptchaAI examples, control operations, and serializer/enum references [2].

## Provider selection

Standard solver instances accept a service type for 2Captcha, RuCaptcha, or DeathByCaptcha, while the README documents CaptchaAI-compatible usage for supported high-level classes and recommends the native client for provider methods not represented by those classes [1]. The underlying endpoint mapping is documented in [provider and result contracts](/service-contracts.md).

## Observed import discrepancy

The README examples use imports such as `from python_rucaptcha import HCaptcha` [1]. The current package initializer imports only `__version__`, while solver classes live in individual modules such as `python_rucaptcha.hcaptcha` [3][4]. This is an observed documentation/runtime discrepancy; callers should verify the installed package's import surface before relying on the top-level examples.

## Relationships

* Standard task behavior is described in [standard solver adapters](/standard-solver-adapters.md).
* Native CaptchaAI usage is described in [CaptchaAI native client](/captchaai-native-client.md).
* Sphinx build and packaging ownership are described in [packaging and documentation](/packaging-and-documentation.md).

## Open Questions

* Unknown: Whether top-level solver re-exports are generated or expected through an external packaging step; no such re-export is present in the current `__init__.py` source.

# Citations

[1] `README.md` — Documents installation, solver examples, async usage, provider switching, and CaptchaAI usage.
[2] `docs/index.rst` — Defines the Sphinx toctrees and published example coverage.
[3] `src/python_rucaptcha/__init__.py` — Currently imports only `__version__`.
[4] `src/python_rucaptcha/hcaptcha.py` — Defines the `HCaptcha` class in its module.
