import asyncio

from src.python_rucaptcha.core.enums import HCaptchaEnm
from src.python_rucaptcha.hcaptcha import HCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad911111111111ca81755768608fa758570"

sitekey = "3ceb8624-1970-4e6b-91d5-70317b70b651"
pageurl = "https://rucaptcha.com/demo/hcaptcha"

lemin_captcha = HCaptcha(
    rucaptcha_key=RUCAPTCHA_KEY, sitekey=sitekey, pageurl=pageurl, method=HCaptchaEnm.HCAPTCHA.value
)
result = lemin_captcha.captcha_handler()

print(result)


async def run():
    try:
        lemin_captcha = await HCaptcha(
            rucaptcha_key=RUCAPTCHA_KEY, sitekey=sitekey, pageurl=pageurl, method=HCaptchaEnm.HCAPTCHA.value
        ).aio_captcha_handler()
        print(lemin_captcha)
    except Exception as err:
        print(err)


asyncio.run(run())
