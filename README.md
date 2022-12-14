# python-rucaptcha


![](files/RuCaptcha.png)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a9f7361b29c54bc09189f34e8ed39a9b)](https://app.codacy.com/gh/AndreiDrang/python-rucaptcha?utm_source=github.com&utm_medium=referral&utm_content=AndreiDrang/python-rucaptcha&utm_campaign=Badge_Grade_Settings)
[![PyPI version](https://badge.fury.io/py/python-rucaptcha.svg)](https://badge.fury.io/py/python-rucaptcha)
[![Python versions](https://img.shields.io/pypi/pyversions/python-rucaptcha.svg?logo=python&logoColor=FBE072)](https://badge.fury.io/py/python-rucaptcha)
[![Downloads](https://pepy.tech/badge/python-rucaptcha/month)](https://pepy.tech/project/python-rucaptcha)

[![Maintainability](https://api.codeclimate.com/v1/badges/aec93bb04a277cf0dde9/maintainability)](https://codeclimate.com/github/AndreiDrang/python-rucaptcha/maintainability)

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
### Changelog

v.4.0 - Rework classes and methods. Adding `TikTok` captcha. Adding inheritance and serializers. The `Callback server` is deprecated.

v.4.2 - Added [Yandex Smart Captcha](https://rucaptcha.com/api-rucaptcha#yandex).

***

## [All examples of working with the library](src/examples)

***

To test various types of captcha, a [special site](https://pythoncaptcha.xyz/) is provided, which contains all available types of captcha, with a convenient system for testing your scripts.

***

### Errors description

1. https://rucaptcha.com/api-rucaptcha#in_errors
2. https://rucaptcha.docs.apiary.io/#reference/2

### Get API Key to work with the library
1. On the page - https://rucaptcha.com/enterpage
2. Find it: ![img.png](files/img.png)
