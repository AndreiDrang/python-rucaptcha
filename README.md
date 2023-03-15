# python-rucaptcha


![](files/RuCaptcha.png)

[![PyPI version](https://badge.fury.io/py/python-rucaptcha.svg)](https://badge.fury.io/py/python-rucaptcha)
[![Python versions](https://img.shields.io/pypi/pyversions/python-rucaptcha.svg?logo=python&logoColor=FBE072)](https://badge.fury.io/py/python-rucaptcha)
[![Downloads](https://pepy.tech/badge/python-rucaptcha/month)](https://pepy.tech/project/python-rucaptcha)

[![Maintainability](https://api.codeclimate.com/v1/badges/aec93bb04a277cf0dde9/maintainability)](https://codeclimate.com/github/AndreiDrang/python-rucaptcha/maintainability)
[![codecov](https://codecov.io/gh/AndreiDrang/python-rucaptcha/branch/master/graph/badge.svg?token=doybTUCfbD)](https://codecov.io/gh/AndreiDrang/python-rucaptcha)

[![Tests](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/test.yml)
[![Lint](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/lint.yml/badge.svg?branch=master)](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/lint.yml)

Python3 library for [RuCaptcha](https://rucaptcha.com/) and [2Captcha](https://2captcha.com/) service API.

Tested on UNIX based OS.

The library is intended for software developers and is used to work with the [RuCaptcha](https://rucaptcha.com/) and [2Captcha](https://2captcha.com/) service API.

***

Application in [RuCaptcha software](https://rucaptcha.com/software/python-rucaptcha) and [2Captcha software](https://2captcha.com/software/python-rucaptcha).

If you have any questions, please send a message to the [Telegram](https://t.me/pythoncaptcha) chat room.

Or email python-captcha@pm.me

***


## How to install?

### pip

```bash
pip install python-rucaptcha
```

### Source
```bash
git clone https://github.com/AndreiDrang/python-rucaptcha.git
cd python-rucaptcha
python setup.py install
```

## How to test?

1. You need set ``API_KEY`` in your environment(get this value from you account).
2. Run command ``make tests``, from root directory.


### Changelog

- v.5.1 - Check [releases page](https://github.com/AndreiDrang/python-rucaptcha/releases).
- v.5.0 - Added AmazonWAF captcha method.
- v.4.2 - Added [Yandex Smart Captcha](https://rucaptcha.com/api-rucaptcha#yandex).
- v.4.0 - Rework classes and methods. Adding `TikTok` captcha. Adding inheritance and serializers. The `Callback server` is deprecated.

### Get API Key to work with the library
1. On the page - https://rucaptcha.com/enterpage
2. Find it: ![img.png](files/img.png)
