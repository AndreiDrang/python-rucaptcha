# python-rucaptcha

![Logo](https://red-panda-dev.xyz/media/original_images/RuCaptchaHigh.png)

<a href="https://dashboard.capsolver.com/passport/register?inviteCode=kQTn-tG07Jb1">
    <img src="https://cdn.discordapp.com/attachments/1105172394655625306/1105180101802471575/20221207-160749.gif" alt="Capsolver's Banner">
</a>
<br>
At the lowest price on the market, you may receive a variety of solutions, including reCAPTCHA V2, reCAPTCHA V3, hCaptcha, hCaptcha Click, FunCaptcha, picture-to-text, and more. With this service, 0.1s is the slowest speed ever measured.
<hr>

[![PyPI version](https://badge.fury.io/py/python-rucaptcha.svg)](https://badge.fury.io/py/python-rucaptcha)
[![Python versions](https://img.shields.io/pypi/pyversions/python-rucaptcha.svg?logo=python&logoColor=FBE072)](https://badge.fury.io/py/python-rucaptcha)
[![Downloads](https://static.pepy.tech/badge/python-rucaptcha/month)](https://pepy.tech/project/python-rucaptcha)

[![Maintainability](https://api.codeclimate.com/v1/badges/aec93bb04a277cf0dde9/maintainability)](https://codeclimate.com/github/AndreiDrang/python-rucaptcha/maintainability)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b4087362bd024b088b358b3e10e7a62f)](https://www.codacy.com/gh/AndreiDrang/python-rucaptcha/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AndreiDrang/python-rucaptcha&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/AndreiDrang/python-rucaptcha/branch/master/graph/badge.svg?token=doybTUCfbD)](https://codecov.io/gh/AndreiDrang/python-rucaptcha)

[![Sphinx docs](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/sphinx.yml/badge.svg?branch=release)](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/sphinx.yml)
[![Build](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/build.yml)
[![Installation](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/install.yml/badge.svg?branch=master)](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/install.yml)
[![Tests](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/test.yml)
[![Lint](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/lint.yml/badge.svg?branch=master)](https://github.com/AndreiDrang/python-rucaptcha/actions/workflows/lint.yml)

Python3 library for [RuCaptcha](https://rucaptcha.com/) and [2Captcha](https://2captcha.com/) service API.

Tested on UNIX based OS.

The library is intended for software developers and is used to work with the [RuCaptcha](https://rucaptcha.com/) and [2Captcha](https://2captcha.com/) service API.

Support of the service [Death By Captcha](https://deathbycaptcha.com?refid=1237267242) is integrated into this library, more information in the library documentation or in the [service docs](https://deathbycaptcha.com/api/2captcha?refid=1237267242).
***

Application in [RuCaptcha software](https://rucaptcha.com/software/python-rucaptcha) and [2Captcha software](https://2captcha.com/software/python-rucaptcha).

If you have any questions, please send a message to the [Telegram](https://t.me/pythoncaptcha) chat room.

Or email python-captcha@pm.me

***

You can check our other projects here - [RedPandaDev group](https://red-panda-dev.xyz/blog/). For example - [Torrents Tracker bot](https://t.me/torrents_tracker_bot) for Telegram.

***


## How to install?

### pip

```bash
pip install python-rucaptcha
```


## How to use?

Is described in the [documentation-website](https://andreidrang.github.io/python-rucaptcha/).

## How to test?

1. You need set ``RUCAPTCHA_KEY`` in your environment(get this value from you account).
2. Run command ``make tests``, from root directory.


### Changelog

For full changelog info check - [Releases page](https://github.com/AndreiDrang/python-rucaptcha/releases).

- v.6.0 - Library refactoring. Stop using `pydantic`, start using `msgspec`. Move to API v2. Drop Python 3.8 support. More details at [Releases page](https://github.com/AndreiDrang/python-rucaptcha/releases). 
- v.5.3 - Added support for [Death By Captcha](https://www.deathbycaptcha.com?refid=1237267242) and other services by changing `service_type` and `url_request` \ `url_response` parameters.
- v.5.2 - Added Audio captcha method.
- v.5.1 - Check [releases page](https://github.com/AndreiDrang/python-rucaptcha/releases).
- v.5.0 - Added AmazonWAF captcha method.
- v.4.2 - Added [Yandex Smart Captcha](https://rucaptcha.com/api-rucaptcha#yandex).

### Get API Key to work with the library
1. On the page - https://rucaptcha.com/enterpage
2. Find it: ![img.png](https://github.com/AndreiDrang/python-rucaptcha/blob/master/files/img.png)
