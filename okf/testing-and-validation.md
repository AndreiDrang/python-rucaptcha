---
type: Validation Process
title: Testing and validation

description: Credential-dependent integration tests, focused checks, linting, builds, and CI validation for the library.
tags: [testing, ci, lint, integration]
source_paths:
  - tests/AGENTS.md
  - tests/conftest.py
  - tests/test_core.py
  - Makefile
  - .github/workflows/test.yml
  - .github/workflows/lint.yml
  - .github/workflows/build.yml
confidence: observed
---

# Testing and validation

## Test model

The test suite exercises the real service-facing library rather than being entirely offline [1]. `tests/conftest.py` reads `RUCAPTCHA_KEY` while defining the base fixture class, so missing credentials can prevent ordinary collection; DeathByCaptcha coverage uses `DEATHBYCAPTCHA_KEY` when available [2]. Function and class fixtures intentionally sleep between tests to throttle cases [2].

Coverage is organized by solver module, with `test_core.py` covering retry object types, context-manager construction, enum helpers, attempt generation, and DeathByCaptcha initialization [3].

## Local commands

* `make lint` checks autoflake, Black, and isort over `src/` [4].
* `make tests` installs the package, runs pytest with coverage, and produces terminal, HTML, and XML coverage reports [4].
* `make build` builds package artifacts after upgrading build tooling [4].
* `make doc` installs the package and builds Sphinx documentation [4].

## CI matrix

The test workflow runs on Python 3.11 with provider credentials supplied as secrets and uploads coverage reports [5]. Lint runs on Python 3.12 [6]. Build checks run on Python 3.9 through 3.12 [7].

## Relationships

* Core behavior under test is described in [request lifecycle](/request-lifecycle.md).
* Packaging and documentation checks are described in [packaging and documentation](/packaging-and-documentation.md).
* New solver work is expected to add matching test coverage [8].

# Citations

[1] `tests/AGENTS.md` — Describes the live service-facing test model and validation guidance.
[2] `tests/conftest.py` — Defines credential access and deliberate test delays.
[3] `tests/test_core.py` — Shows representative foundation tests and expected helper behavior.
[4] `Makefile` — Defines lint, test, build, and documentation commands.
[5] `.github/workflows/test.yml` — Defines test CI, Python version, secrets, and coverage uploads.
[6] `.github/workflows/lint.yml` — Defines lint CI on Python 3.12.
[7] `.github/workflows/build.yml` — Defines build CI for Python 3.9–3.12.
[8] `src/python_rucaptcha/AGENTS.md` — Requires a matching test module for new CAPTCHA types.
