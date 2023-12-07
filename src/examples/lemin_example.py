import asyncio

from python_rucaptcha.core.enums import LeminCroppedCaptchaEnm
from python_rucaptcha.lemin_captcha import LeminCroppedCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad9053f111111111111111fa758570"

pageurl = "https://dashboard.leminnow.com/auth/signup"
api_server = "api.leminnow.com"
div_id = "lemin-cropped-captcha"
captcha_id = "CROPPED_099216d_8ba061383fa24ef498115023aa7189d4"

lemin_captcha = LeminCroppedCaptcha(
    rucaptcha_key=RUCAPTCHA_KEY,
    pageurl=pageurl,
    captcha_id=captcha_id,
    div_id=div_id,
    method=LeminCroppedCaptchaEnm.LEMIN.value,
    api_server=api_server,
)
result = lemin_captcha.captcha_handler()

print(result)


async def run():
    try:
        lemin_captcha = await LeminCroppedCaptcha(
            rucaptcha_key=RUCAPTCHA_KEY,
            pageurl=pageurl,
            captcha_id=captcha_id,
            div_id=div_id,
            method=LeminCroppedCaptchaEnm.LEMIN.value,
            api_server=api_server,
        ).aio_captcha_handler()
        print(lemin_captcha)
    except Exception as err:
        print(err)


asyncio.run(run())
