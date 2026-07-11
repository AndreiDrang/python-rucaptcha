# AGENTS.md

## Scope and inheritance

Applies to: `src/python_rucaptcha/` and its descendants.

Inherits repository-wide guidance from `../../AGENTS.md`.

This file defines only local differences for this package subtree.

## What lives here

```text
src/python_rucaptcha/
├── *_captcha.py        # Concrete CAPTCHA task builders and handlers (inherit BaseCaptcha)
├── captchaai.py        # Native CaptchaAI client — data-driven, NOT a BaseCaptcha solver
├── control.py          # Balance/status-style service operations
├── __init__.py         # Package re-exports
├── __version__.py      # Single source of the package version
└── core/               # Shared request flow, serializers, enums, CaptchaAI profile data
```

## Local boundaries and invariants

- Concrete modules are deliberately flat and inherit from `core.base.BaseCaptcha`.
- A solver owns its service task fields, method validation, and sync/async handler entry points; shared transport and polling remain in `core/`.
- Keep module names in the existing `*_captcha.py` style and enum names in the `{CaptchaType}Enm` style, including established exceptions such as `re_captcha.py` and `hcaptcha.py`.
- `captchaai.py` is the deliberate exception to the `BaseCaptcha` pattern: it is a data-driven native client that validates against packaged profiles in `core/data/` and passes provider-native params through. Do not merge it into `BaseCaptcha`, and do not add per-method task branches to it.

## Safe change rules

When adding a CAPTCHA type, add the module, its enum in `core/enums.py`, a corresponding `tests/test_<captcha>.py`, and the relevant `docs/modules/*` example/toctree entry. Reuse `BaseCaptcha` rather than introducing a second transport path.

Before changing a core call or payload contract for one solver, inspect the sibling modules and the shared core instruction file; a local workaround should not become a global branch.

## Validation

For focused feedback, run the matching test module, for example `pytest tests/test_hcaptcha.py`, then use the root-level `make lint` and `make tests` checks as appropriate. API-key and live-service requirements are documented in `tests/AGENTS.md`.
