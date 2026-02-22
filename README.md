# python-rucaptcha

[![PyPI version](https://badge.fury.io/py/python-rucaptcha.svg)](https://badge.fury.io/py/python-rucaptcha)
[![Python versions](https://img.shields.io/pypi/pyversions/python-rucaptcha.svg?logo=python&logoColor=FBE072)](https://badge.fury.io/py/python-rucaptcha)
[![Downloads](https://static.pepy.tech/badge/python-rucaptcha/month)](https://pepy.tech/project/python-rucaptcha)
[![Documentation](https://img.shields.io/badge/docs-Sphinx-green)](https://andreidrang.github.io/python-rucaptcha/)

**Python 3.9+ library to solve CAPTCHAs automatically using RuCaptcha, 2Captcha, or DeathByCaptcha services.**

## What is this?

This library automates CAPTCHA solving by connecting to third-party services. When your code encounters a CAPTCHA, python-rucaptcha sends it to the service, waits for a human to solve it, and returns the solution to your application.

**Supports 30+ CAPTCHA types:**
- reCAPTCHA v2/v3, hCaptcha, Cloudflare Turnstile
- Image captchas, Audio captchas
- GeeTest, KeyCaptcha, Amazon WAF, Tencent
- And many more...

## Quick Start

### 1. Install

```bash
pip install python-rucaptcha
```

### 2. Get an API Key

Sign up at [RuCaptcha](https://rucaptcha.com) or [2Captcha](https://2captcha.com), then copy your API key from the dashboard.

### 3. Solve a CAPTCHA

```python
from python_rucaptcha import HCaptcha

# Your API key
key = "your_api_key_here"

# Solve hCaptcha
result = HCaptcha(aptcha_key=key).captcha_handler(site_url="https://example.com", site_key="abc123")

if result['code'] == 0:
    print(f"Solved! Token: {result['token']}")
else:
    print(f"Error: {result['message']}")
```

### Solving Different CAPTCHA Types

**reCAPTCHA v2:**
```python
from python_rucaptcha import ReCaptcha

result = ReCaptcha(api_key).captcha_handler(
    site_url="https://example.com",
    site_key="your_site_key"
)
```

**Image CAPTCHA:**
```python
from python_rucaptcha import ImageCaptcha

result = ImageCaptcha(api_key).captcha_handler(
    image_link="https://example.com/captcha.jpg"
)
```

**Using async:**
```python
import asyncio
from python_rucaptcha import HCaptcha

async def solve():
    result = await HCaptcha(api_key).aio_captcha_handler(
        site_url="https://example.com",
        site_key="abc123"
    )
    return result

token = asyncio.run(solve())
```

## Supported CAPTCHA Types

| CAPTCHA | Module | Description |
|---------|--------|-------------|
| reCAPTCHA v2/v3 | `ReCaptcha` | Google reCAPTCHA |
| hCaptcha | `HCaptcha` | hCaptcha challenge |
| Cloudflare Turnstile | `Turnstile` | Cloudflare protection |
| Image | `ImageCaptcha` | Type the text from image |
| Audio | `AudioCaptcha` | Listen and type audio |
| GeeTest | `GeeTest` | Chinese geetest puzzles |
| KeyCaptcha | `KeyCaptcha` | KeyCAPTCHA service |
| Amazon WAF | `AmazonWaf` | AWS WAF challenge |
| Grid | `GridCaptcha` | Select grid cells |
| Coordinates | `CoordinatesCaptcha` | Click on coordinates |
| And 20+ more | ... | See [full docs](https://andreidrang.github.io/python-rucaptcha/) |

## Switching Services

Use the same code with different services:

```python
from python_rucaptcha import HCaptcha
from python_rucaptcha.core.enums import ServiceEnm

# Use 2Captcha (default)
result = HCaptcha("2captcha_key").captcha_handler(...)

# Use RuCaptcha
result = HCaptcha("rucaptcha_key", service_type=ServiceEnm.RuCaptcha).captcha_handler(...)

# Use DeathByCaptcha
result = HCaptcha("dbc_user:dbc_pass", service_type=ServiceEnm.DeathByCaptcha).captcha_handler(...)
```

## Testing

```bash
# Set your API key
export RUCAPTCHA_KEY="your_key_here"

# Run tests
make tests
```

## Documentation

For advanced usage, configuration options, and all CAPTCHA types, see the [full documentation](https://andreidrang.github.io/python-rucaptcha/).

## Support

- **Telegram:** [pythoncaptcha](https://t.me/pythoncaptcha)
- **Email:** python-captcha@pm.me
- **Issues:** [GitHub Issues](https://github.com/AndreiDrang/python-rucaptcha/issues)

## Changelog

See [Releases](https://github.com/AndreiDrang/python-rucaptcha/releases) for full changelog.

- **v6.0** - Refactored to use msgspec (faster), API v2, dropped Python 3.8
- **v5.3** - Added DeathByCaptcha support
- **v5.2** - Added audio CAPTCHA solving
