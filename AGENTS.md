# AGENTS.md

## Repository overview

- `python-rucaptcha` is a Python 3.9+ setuptools library for the 2Captcha, RuCaptcha, DeathByCaptcha, and CaptchaAI APIs.
- The project is a single `src/`-layout package, not a monorepo, with synchronous and asynchronous solver handlers.
- Remote provider APIs are the runtime boundary; the repository has no service, worker, queue, or database runtime.

## Instruction scope

- This root `AGENTS.md` applies repository-wide. A nearer `AGENTS.md` adds local guidance for its subtree; sibling files do not affect one another.
- Current local instruction files are `src/python_rucaptcha/AGENTS.md`, `src/python_rucaptcha/core/AGENTS.md`, `tests/AGENTS.md`, and `docs/AGENTS.md`.
- No `AGENTS.override.md` is currently used. If one is introduced, it takes precedence over `AGENTS.md` in the same directory and must state its explicit override.

## Where to work

```text
src/python_rucaptcha/       # flat solver adapters and package API
└── core/                   # shared transport, contracts, enums, and CaptchaAI data
 tests/                     # credential-dependent solver and core tests
 docs/                      # Sphinx configuration and per-CAPTCHA examples
 .github/workflows/         # install, test, lint, build, and docs CI
 pyproject.toml             # setuptools, Black, isort, and pytest configuration
 Makefile                   # install, lint, test, build, and documentation workflows
```

Do not hand-edit `dist/`, build/coverage output, or `src/python_rucaptcha.egg-info/`.

## Architecture and boundaries

- Concrete solver modules prepare CAPTCHA-specific task fields and inherit the shared flow from `src/python_rucaptcha/core/base.py`; keep provider-specific payload logic out of the shared core.
- `core/` owns request/polling behavior, retry configuration, service URL selection, msgspec serialization, result models, and shared enums. Changes there can affect every solver.
- Synchronous and asynchronous handlers for a solver must keep the same task semantics and normalized response shape; remote service field names are part of the public contract.
- The native CaptchaAI client (`src/python_rucaptcha/captchaai.py` plus `core/captchaai.py`) is intentionally separate from `BaseCaptcha`: it uses the classic multipart API and packaged JSON profiles. Do not convert it to per-method branches or the generic task flow.

## Context routing

Read only when relevant:

- Public usage, supported services, or user-facing claims → `README.md`.
- Cross-module architecture, dependency direction, or request flows → `ARCHITECTURE.md`.
- Contribution expectations → `CONTRIBUTING.md`.
- Documentation navigation, autodoc imports, or Sphinx settings → `docs/index.rst`, `docs/conf.py`, and `docs/AGENTS.md`.
- Core transport, serializer, enum, result, or CaptchaAI profile changes → `src/python_rucaptcha/core/AGENTS.md` and the relevant core modules.
- Test fixture or integration behavior → `tests/AGENTS.md` and `tests/conftest.py`.
- Detailed local architecture notes, when cited by architecture work → the relevant file under `okf/`.

## Change rules

- Adding a solver normally requires a package module, a matching enum in `core/enums.py`, a `tests/test_<captcha>.py` module, and a `docs/modules/` example plus `docs/index.rst` toctree entry when user-facing.
- Preserve the existing flat module and naming conventions, including established modules such as `re_captcha.py` and `hcaptcha.py`, and `{CaptchaType}Enm` enum names.
- Do not add solver-specific branches to `BaseCaptcha`; inspect sibling adapters before changing shared payload or call behavior.
- Changes to CaptchaAI profile JSON must preserve both runtime files and the `tool.setuptools.package-data` declaration in `pyproject.toml`.
- Never commit API keys or add diagnostics that expose credentials or complete provider responses unnecessarily.

## Validation

- Formatting/static checks: `make lint` (autoflake, Black, and isort over `src/`).
- Focused tests: `pytest tests/test_<captcha>.py`; core changes start with `pytest tests/test_core.py` and add affected solver tests.
- Full integration/coverage suite: `make tests`; it installs the package, runs pytest, and requires `RUCAPTCHA_KEY` (and `DEATHBYCAPTCHA_KEY` for relevant coverage).
- Package and docs checks: `make build` and `make doc`.
- CI tests on Python 3.11, lint on 3.12, build/install on Python 3.9–3.12, and docs on 3.12; use the workflow files as the current source for CI details.

## Repository-specific gotchas

- `tests/conftest.py` reads `RUCAPTCHA_KEY` while defining `BaseTest`, so missing credentials can prevent normal pytest collection rather than merely skip tests.
- Test fixtures intentionally sleep between cases; use focused tests while iterating, then run the relevant full command before handoff.
- `src/python_rucaptcha/__init__.py` currently exports the package version only; verify actual module exports before relying on README examples that import solvers from the package root.
