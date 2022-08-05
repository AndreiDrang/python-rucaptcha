import asyncio

from src.python_rucaptcha.enums import LeminCroppedCaptchaEnm
from src.python_rucaptcha.LeminCroppedCaptcha import LeminCroppedCaptcha, aioLeminCroppedCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad9053f111111111111111fa758570"


pageurl = "https://dashboard.leminnow.com/auth/signup"
api_server = "https://api.leminnow.com/"
div_id = "jOfjiAwLlemin-captcha-input-box"
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
        lemin_captcha = await aioLeminCroppedCaptcha(
            rucaptcha_key=RUCAPTCHA_KEY,
            pageurl=pageurl,
            captcha_id=captcha_id,
            div_id=div_id,
            method=LeminCroppedCaptchaEnm.LEMIN.value,
            api_server=api_server,
        ).captcha_handler()
        print(lemin_captcha)
    except Exception as err:
        print(err)


asyncio.run(run())
