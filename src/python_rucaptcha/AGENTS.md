# python_rucaptcha Package

**Parent:** ./AGENTS.md

## OVERVIEW
Main package containing 30+ CAPTCHA solver modules. Each module implements a specific CAPTCHA type.

## STRUCTURE
```
src/python_rucaptcha/
├── __init__.py           # Exports __version__, package info
├── core/                 # Base classes (base.py, config.py, enums.py, serializer.py)
├── _captcha.py          # Internal helpers
├── hcaptcha.py          # hCaptcha solver
├── re_captcha.py        # reCaptcha v2/v3 solver
├── turnstile.py         # Cloudflare Turnstile solver
├── image_captcha.py     # Image captcha solver
├── audio_captcha.py     # Audio captcha solver
├── gee_test.py          # GeeTest solver
├── key_captcha.py       # KeyCaptcha solver
├── ...                  # 20+ more captcha types
└── control.py          # Balance/status checker
```

## WHERE TO LOOK
| Task | File |
|------|------|
| Add new CAPTCHA type | Create new `*_captcha.py` module |
| Modify BaseCaptcha | `core/base.py` |
| Add new enum | `core/enums.py` |

## CONVENTIONS
- **Module naming**: `*_captcha.py` pattern
- **Class naming**: `{CaptchaType}Captcha` (e.g., `HCaptcha`, `ReCaptcha`)
- **Enum naming**: `{CaptchaType}Enm` (e.g., `HCaptchaEnm`)
- **Inheritance**: All captcha classes extend `BaseCaptcha`

## ADDING NEW CAPTCHA
1. Create `src/python_rucaptcha/new_captcha.py`
2. Define enum `NewCaptchaEnm` in `core/enums.py`
3. Create class `NewCaptcha(BaseCaptcha)` implementing required methods
4. Add tests in `tests/test_new_captcha.py`

## ANTI-PATTERNS
- DO NOT modify core files without understanding the inheritance chain
- DO NOT add captcha-specific logic directly in BaseCaptcha
