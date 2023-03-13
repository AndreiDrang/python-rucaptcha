import asyncio

from python_rucaptcha.core.enums import ReCaptchaEnm
from python_rucaptcha.re_captcha import ReCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad9053f111111111111111fa758570"

# ReCaptchaV3

googlekey = "6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH"
pageurl = "https://rucaptcha.com/demo/recaptcha-v2"

re_captcha = ReCaptcha(
    rucaptcha_key=RUCAPTCHA_KEY,
    pageurl=pageurl,
    googlekey=googlekey,
    method=ReCaptchaEnm.USER_RECAPTCHA.value,
)
result = re_captcha.captcha_handler()

print(result)


async def run():
    try:
        re_captcha = await ReCaptcha(
            rucaptcha_key=RUCAPTCHA_KEY,
            pageurl=pageurl,
            googlekey=googlekey,
            method=ReCaptchaEnm.USER_RECAPTCHA.value,
        ).aio_captcha_handler()
        print(re_captcha)
    except Exception as err:
        print(err)


asyncio.run(run())

# ReCaptchaV3 invisible
googlekey = "6LfDxboZAAAAAD6GHukjvUy6lszoeG3H4nQW57b6"
pageurl = "https://rucaptcha.com/demo/recaptcha-v2-invisible"

re_captcha = ReCaptcha(
    rucaptcha_key=RUCAPTCHA_KEY,
    pageurl=pageurl,
    googlekey=googlekey,
    method=ReCaptchaEnm.USER_RECAPTCHA.value,
    invisible=1,
)
result = re_captcha.captcha_handler()

print(result)


async def run():
    try:
        re_captcha = await ReCaptcha(
            rucaptcha_key=RUCAPTCHA_KEY,
            pageurl=pageurl,
            googlekey=googlekey,
            method=ReCaptchaEnm.USER_RECAPTCHA.value,
            invisible=1,
        ).aio_captcha_handler()
        print(re_captcha)
    except Exception as err:
        print(err)


asyncio.run(run())

# ReCaptchaV3

googlekey = "6LfB5_IbAAAAAMCtsjEHEHKqcB9iQocwwxTiihJu"
pageurl = "https://rucaptcha.com/demo/recaptcha-v3"
version = "v3"
action = "demo_action"
score = 0.1

re_captcha = ReCaptcha(
    rucaptcha_key=RUCAPTCHA_KEY,
    pageurl=pageurl,
    googlekey=googlekey,
    method=ReCaptchaEnm.USER_RECAPTCHA.value,
    version=version,
    action=action,
    score=score,
)
result = re_captcha.captcha_handler()

print(result)


async def run():
    try:
        re_captcha = await aioReCaptcha(
            rucaptcha_key=RUCAPTCHA_KEY,
            pageurl=pageurl,
            googlekey=googlekey,
            method=ReCaptchaEnm.USER_RECAPTCHA.value,
            version=version,
            action=action,
            score=score,
        ).captcha_handler()
        print(re_captcha)
    except Exception as err:
        print(err)


asyncio.run(run())
