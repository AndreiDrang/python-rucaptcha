# AGENTS.md

## Repository overview

- `python-rucaptcha` is a Python 3.9+ setuptools library for the 2Captcha, RuCaptcha, DeathByCaptcha, and CaptchaAI APIs.
- The package uses a `src/` layout and provides synchronous and asynchronous CAPTCHA solver handlers.
- The repository is a single package, not a monorepo. The root `AGENTS.md` applies everywhere unless a nearer local file applies.

## Instruction scope

- Local instruction files are `src/python_rucaptcha/AGENTS.md`, `src/python_rucaptcha/core/AGENTS.md`, `tests/AGENTS.md`, and `docs/AGENTS.md`.
- A nearer `AGENTS.md` adds local guidance; it does not repeat or silently contradict this file. Sibling files do not affect one another.
- No `AGENTS.override.md` files are present. If one is introduced, it takes precedence only within its own directory.

## Where to work

```text
src/python_rucaptcha/       # CAPTCHA implementations and package API
└── core/                   # Base request flow, service config, serializers, enums, CaptchaAI profile data
 tests/                     # Pytest suite and shared fixtures
 docs/                      # Sphinx sources and per-CAPTCHA examples
 pyproject.toml             # setuptools, Black, isort, and pytest configuration
 Makefile                   # install, lint, test, build, and documentation workflows
```

Do not hand-edit `dist/` or `src/python_rucaptcha.egg-info/`; they are build/package metadata outputs.

## Architecture and boundaries

- Concrete CAPTCHA modules inherit from `BaseCaptcha` in `src/python_rucaptcha/core/base.py`. Keep CAPTCHA-specific payload preparation in the concrete module, not in the shared base flow.
- `core/` owns request/polling behavior, service URL selection, msgspec serialization, result models, and shared enums. Changes there can affect every solver.
- Each solver's synchronous and asynchronous handlers must preserve the same task semantics and response shape. Service task field names are part of the external API contract.
- The data-driven `captchaai` client (top-level `captchaai.py` + `core/captchaai.py`) is deliberately separate from the `BaseCaptcha` flow: it validates packaged JSON profiles in `core/data/` instead of branching on task types. Do not refactor it into the `BaseCaptcha` pattern or add per-method branches to it.

## Context routing

- For public usage and supported solver/service behavior, read `README.md`.
- For contribution expectations, read `CONTRIBUTING.md` before preparing a project-wide change.
- For documentation changes, read `docs/index.rst` and `docs/conf.py`; the local rules are in `docs/AGENTS.md`.
- For build, formatting, test, or packaging changes, read `pyproject.toml`, `Makefile`, and the relevant `.github/workflows/*.yml` file.
- No `ARCHITECTURE.md` is present; use the core modules and package-local instructions as the current implementation source of truth.

## Change rules

- Adding a solver normally requires a new package module, a matching enum in `core/enums.py`, tests under `tests/`, and a documentation example/toctree entry when it is user-facing.
- Preserve the existing flat `*_captcha.py` module naming and `{CaptchaType}Captcha`/`{CaptchaType}Enm` naming patterns.
- Do not put solver-specific branches into `BaseCaptcha` merely to support one CAPTCHA type.
- Never commit API keys or add diagnostics that expose credentials or complete service responses unnecessarily. The integration tests make external service calls.

## Validation

- Formatting/static checks: `make lint` (autoflake, Black, and isort over `src/`).
- Integration tests and coverage: `make tests`; collection requires `RUCAPTCHA_KEY`, and DeathByCaptcha coverage may use `DEATHBYCAPTCHA_KEY`.
- Package build: `make build`.
- Sphinx documentation: `make doc`.
- CI runs tests on Python 3.11, lint on 3.12, and build checks on Python 3.9–3.12; account for the supported `requires-python >= 3.9` range.

## Repository-specific gotchas

- `tests/conftest.py` reads `RUCAPTCHA_KEY` while defining `BaseTest`, so missing credentials can prevent normal test collection rather than merely skip a test.
- The test fixtures deliberately sleep between cases and the suite is not an offline-only unit suite; use targeted tests while iterating, then run the relevant full command before handoff.
