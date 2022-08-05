import asyncio

from src.python_rucaptcha.enums import HCaptchaEnm
from src.python_rucaptcha.HCaptcha import HCaptcha, aioHCaptcha

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
        lemin_captcha = await aioHCaptcha(
            rucaptcha_key=RUCAPTCHA_KEY, sitekey=sitekey, pageurl=pageurl, method=HCaptchaEnm.HCAPTCHA.value
        ).captcha_handler()
        print(lemin_captcha)
    except Exception as err:
        print(err)


asyncio.run(run())
