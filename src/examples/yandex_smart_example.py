import asyncio

from python_rucaptcha.core.enums import YandexSmartCaptchaEnm
from python_rucaptcha.YandexSmartCaptcha import YandexSmartCaptcha, aioYandexSmartCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad9053f111111111111111fa758570"

# YandexSmartCaptcha

sitekey = "AbC0defgHiJKLm12Opq34rst5uV6w7XYzaBcdE8f"
pageurl = "http://mysite.com/page_with_yandex"

ya_captcha = YandexSmartCaptcha(
    rucaptcha_key=RUCAPTCHA_KEY,
    pageurl=pageurl,
    sitekey=sitekey,
    method=YandexSmartCaptchaEnm.YANDEX.value,
)
result = ya_captcha.captcha_handler()

print(result)


async def run():
    try:
        ya_captcha = await aioYandexSmartCaptcha(
            rucaptcha_key=RUCAPTCHA_KEY,
            pageurl=pageurl,
            sitekey=sitekey,
            method=YandexSmartCaptchaEnm.YANDEX.value,
        ).captcha_handler()
        print(ya_captcha)
    except Exception as err:
        print(err)


asyncio.run(run())
