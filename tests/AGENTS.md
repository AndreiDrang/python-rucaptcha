# tests Package

**Parent:** ./AGENTS.md

## OVERVIEW
Pytest test suite with 23+ test files covering all CAPTCHA types.

## STRUCTURE
```
tests/
├── __init__.py
├── conftest.py           # Fixtures + BaseTest class
├── test_core.py          # BaseCaptcha tests
├── test_hcaptcha.py      # hCaptcha tests
├── test_recaptcha.py     # reCaptcha tests
├── test_turnstile.py     # Turnstile tests
├── ...                   # 20+ more test files
└── test_image.py         # Image captcha tests
```

## WHERE TO LOOK
| Task | File |
|------|------|
| Add new test | Create `test_{captcha}.py` |
| Test fixtures | `conftest.py` |

## CONVENTIONS
- **File naming**: `test_*.py` pattern
- **Test class**: Extend `BaseTest` from `conftest.py`
- **Run**: `make tests` or `pytest tests/`

## TEST REQUIREMENTS
- Requires `RUCAPTCHA_KEY` environment variable
- Optional: `DEATHBYCAPTCHA_KEY` for DeathByCaptcha tests
- Tests make real API calls to captcha services

## FIXTURES (conftest.py)
- `delay_func`: 0.5s sleep (function scope)
- `delay_class`: 3s sleep (class scope)
- `BaseTest`: Base test class with required env var check
- `DeathByTest`: Subclass with optional DEATHBYCAPTCHA_KEY
