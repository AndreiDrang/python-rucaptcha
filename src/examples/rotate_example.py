import asyncio

from python_rucaptcha.core.enums import RotateCaptchaEnm
from python_rucaptcha.rotate_captcha import RotateCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad911111111111ca81755768608fa758570"

captcha_url = "https://rucaptcha.com/dist/web/b771cc7c5eb0c1a811fcb91d54e4443a.png"
captcha_path = "src/examples/rotate/rotate_ex.png"

rotate_captcha = RotateCaptcha(rucaptcha_key=RUCAPTCHA_KEY, method=RotateCaptchaEnm.ROTATECAPTCHA.value)
# file URL
result = rotate_captcha.captcha_handler(captcha_link=captcha_url)

print(result)

# file path
result = rotate_captcha.captcha_handler(captcha_link=captcha_path)

print(result)

# ASYNC example

rotate_captcha = RotateCaptcha(rucaptcha_key=RUCAPTCHA_KEY, method=RotateCaptchaEnm.ROTATECAPTCHA.value)


async def run():
    # file URL
    result = await rotate_captcha.aio_captcha_handler(captcha_link=captcha_url)

    print(result)

    # file path
    result = await rotate_captcha.aio_captcha_handler(captcha_link=captcha_path)

    print(result)


asyncio.run(run())
