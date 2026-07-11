# AGENTS.md

## Scope and inheritance

Applies to: `tests/` and its descendants.

Inherits repository-wide guidance from `../AGENTS.md`.

This file defines only local differences for the test subtree.

## What lives here

```text
tests/
├── conftest.py       # Environment-dependent fixtures and BaseTest classes
├── test_core.py      # Shared base/config/enum behavior
└── test_<captcha>.py # Coverage organized by solver module
```

## Local boundaries and invariants

- Tests exercise the real service-facing library. `conftest.py` reads `RUCAPTCHA_KEY` during test class definition, and DeathByCaptcha-specific tests use `DEATHBYCAPTCHA_KEY` when available.
- `delay_func` and `delay_class` intentionally throttle cases; do not remove or shorten them just to make the suite look like an offline unit suite.
- New solver coverage belongs in a matching `test_<captcha>.py` module. Reuse `BaseTest` for the shared random-string helper and credential setup; use `DeathByTest` for DeathByCaptcha-specific coverage.

## Safe change rules

When changing a payload, enum, or shared handler, update `test_core.py` or the affected solver test rather than relying only on a live smoke test. Avoid placing real API keys, service responses, or other credentials in fixtures and assertions.

## Validation

For iteration, run a focused module such as `pytest tests/test_hcaptcha.py`. The repository-level `make tests` command installs the package, runs pytest with coverage, and generates coverage artifacts; it requires the environment variables described above.
