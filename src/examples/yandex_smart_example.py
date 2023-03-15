import asyncio

from python_rucaptcha.core.enums import YandexSmartCaptchaEnm
from python_rucaptcha.yandex_smart_captcha import YandexSmartCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad9053f111111111111111fa758570"

# YandexSmartCaptcha

sitekey = "FEXfAbHQsToo97VidNVk3j4dC74nGW1DgdxjtNB9"
pageurl = "https://captcha-api.yandex.ru/demo"

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
        ya_captcha = await YandexSmartCaptcha(
            rucaptcha_key=RUCAPTCHA_KEY,
            pageurl=pageurl,
            sitekey=sitekey,
            method=YandexSmartCaptchaEnm.YANDEX.value,
        ).aio_captcha_handler()
        print(ya_captcha)
    except Exception as err:
        print(err)


asyncio.run(run())
