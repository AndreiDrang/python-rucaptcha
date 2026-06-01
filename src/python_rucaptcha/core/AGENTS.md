# core Module

**Parent:** ../AGENTS.md, ../../src/python_rucaptcha/AGENTS.md

## OVERVIEW
Foundation module with base classes, configuration, serialization, and enums. All captcha solvers depend on these.

## WHERE TO LOOK
| File | Role |
|------|------|
| `base.py` | BaseCaptcha class - parent for all solvers |
| `config.py` | CaptchaOptionsSer - service URL abstraction |
| `serializer.py` | MyBaseModel - msgspec wrapper |
| `enums.py` | MyEnum + 25+ CAPTCHA enums |

## KEY SYMBOLS
- `BaseCaptcha`: Parent class for all captcha solvers (sync + async)
- `MyBaseModel`: msgspec Struct wrapper with `.to_dict()`
- `CaptchaOptionsSer`: Dynamic service URL selection
- `MyEnum`: Custom enum with `.list()`, `.list_values()`, `.list_names()`

## CONVENTIONS
- **BaseCaptcha provides**: `captcha_handler()`, `aio_captcha_handler()`, session management, file handling
- **Serialization**: Uses msgspec (not pydantic)
- **Enums**: Each CAPTCHA type has dedicated enum in enums.py
