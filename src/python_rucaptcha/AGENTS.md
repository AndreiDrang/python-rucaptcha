# AGENTS.md

## Scope and inheritance

Applies to: `src/python_rucaptcha/` and its descendants.

Inherits repository-wide guidance from `../../AGENTS.md`.

This file defines only local differences for this package subtree.

## What lives here

```text
src/python_rucaptcha/
├── *_captcha.py and established flat modules  # Concrete CAPTCHA adapters
├── captchaai.py                              # Native CaptchaAI client; not a BaseCaptcha solver
├── control.py                                # Balance/report-style operations
├── __init__.py                               # Currently exports the package version
├── __version__.py                            # Single source of package version
└── core/                                     # Shared flow, contracts, enums, and profile data
```

## Local boundaries and invariants

- Concrete solver modules own their service task fields, method validation, input preparation, and sync/async handler entry points; shared transport and polling remain in `core/`.
- Most adapters inherit `core.base.BaseCaptcha`. Keep module names in the existing flat style and enum names in the `{CaptchaType}Enm` style, including established modules such as `re_captcha.py` and `hcaptcha.py`.
- `captchaai.py` is the deliberate exception: it is a data-driven native client that validates packaged profiles in `core/data/` and passes provider-native parameters through. Do not merge it into `BaseCaptcha` or add per-method task branches.

## Safe change rules

When adding a CAPTCHA type, add the module, its enum in `core/enums.py`, a matching `tests/test_<captcha>.py`, and the relevant `docs/modules/` example and `docs/index.rst` toctree entry. Reuse `BaseCaptcha` rather than introducing another transport path.

Before changing a shared call or payload contract for one solver, inspect sibling modules and `core/AGENTS.md`; a local workaround should not become a global branch. Verify package-root exports against `__init__.py` rather than assuming README import examples are current.

## Validation

For focused feedback, run the matching test module, for example `pytest tests/test_hcaptcha.py`, then use root-level `make lint` and `make tests` as appropriate. Core changes should also start with `pytest tests/test_core.py`; credential and live-service requirements are documented in `tests/AGENTS.md`.
