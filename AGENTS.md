# PROJECT KNOWLEDGE BASE

**Generated:** 2026-02-20
**Commit:** 86ee3e6
**Branch:** master

## OVERVIEW
Python 3.9+ library for RuCaptcha/2Captcha/DeathByCaptcha service APIs. Supports 30+ CAPTCHA types with dual sync/async interfaces.

## STRUCTURE
```
./
├── src/python_rucaptcha/    # Main package (30+ captcha modules)
│   └── core/                # Base classes, serializers, enums
├── tests/                   # Pytest test suite (23+ files)
├── docs/                    # Sphinx documentation
├── pyproject.toml           # Build config (black 110, isort, pytest)
└── Makefile                 # Build automation
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Add new CAPTCHA | `src/python_rucaptcha/` | Create module inheriting `BaseCaptcha` |
| Modify API flow | `src/python_rucaptcha/core/base.py` | `_processing_response()` methods |
| Change serialization | `src/python_rucaptcha/core/serializer.py` | `MyBaseModel` class |
| Add CAPTCHA enum | `src/python_rucaptcha/core/enums.py` | 25+ enum classes |
| Run tests | `tests/` | Requires `RUCAPTCHA_KEY` env var |

## CODE MAP
| Symbol | Type | Location | Role |
|--------|------|----------|------|
| BaseCaptcha | Class | core/base.py | Parent for all captcha solvers |
| MyBaseModel | Class | core/serializer.py | msgspec Struct wrapper |
| CaptchaOptionsSer | Class | core/config.py | Service URL abstraction |
| MyEnum | Class | core/enums.py | Custom enum with utils |

## CONVENTIONS
- **Line length**: 110 chars (pyproject.toml)
- **Async mode**: `asyncio_mode = auto` in pytest
- **No tox**: Uses Makefile directly for test/lint
- **Import order**: isort with black profile

## ANTI-PATTERNS (THIS PROJECT)
- No TODO/FIXME/DEPRECATED comments in code
- No explicit "DO NOT" directives
- Logging warnings output full result objects (potential sensitive data)

## UNIQUE STYLES
- **25+ custom enums**: Each CAPTCHA type has dedicated enum (e.g., `HCaptchaEnm`)
- **Service abstraction**: Unified API for 2Captcha/RuCaptcha/DeathByCaptcha
- **msgspec**: Fast serialization (replaced pydantic v6.0)
- **Dual sync/async**: Every captcha class has both handlers

## COMMANDS
```bash
make install    # pip install -e .
make tests      # Run pytest with coverage
make lint       # autoflake + black + isort check
make build      # Build package
make doc        # Build Sphinx docs
```

## NOTES
- Tests require live API keys (`RUCAPTCHA_KEY`, `DEATHBYCAPTCHA_KEY`)
- CI runs on Python 3.11 (tests) / 3.12 (lint) — version mismatch
- No cross-platform testing (only ubuntu-latest)
- x.py in root is debug script (non-standard)
