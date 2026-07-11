# AGENTS.md

## Scope and inheritance

Applies to: `src/python_rucaptcha/core/` and its descendants.

Inherits repository-wide guidance from `../../../AGENTS.md` and package-local guidance from `../AGENTS.md`.

This file defines only local differences for this foundation subtree.

## What lives here

```text
core/
├── base.py           # BaseCaptcha sync/async transport, polling, file handling
├── config.py         # Retry settings and application/service configuration
├── serializer.py     # msgspec Struct request/response models
├── enums.py          # Service, task-method, and save-format enums
└── result_handler.py # Sync/async result polling helpers
```

## Local boundaries and invariants

- This is the shared foundation for every solver. `BaseCaptcha` owns task creation, result polling, retries, sessions, and file/base64 preparation for both sync and async paths.
- Request and response models use `msgspec`; preserve `MyBaseModel.to_dict()` behavior and the serialized field names expected by the remote APIs.
- `CaptchaOptionsSer.urls_set()` selects the 2Captcha/RuCaptcha create-task endpoints and the DeathByCaptcha-compatible endpoints. Keep service selection and response/error shapes compatible with concrete modules.
- CAPTCHA-specific behavior belongs in the leaf solver modules, not in `base.py` or another shared model.

## Safe change rules

Treat changes to `base.py`, `serializer.py`, `config.py`, `enums.py`, or `result_handler.py` as cross-package API changes. Check all affected solver modules and update shared/core tests plus representative solver tests; do not replace msgspec with another model system without an explicit repository-wide migration.

## Validation

Start with `pytest tests/test_core.py` for foundation changes and add targeted solver tests for changed payload or handler behavior. Run `make lint` before handoff; live integration requirements are defined by the root and `tests/AGENTS.md`.
