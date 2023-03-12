import asyncio

from src.python_rucaptcha.image_captcha import ImageCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad911111111111ca81755768608fa758570"

captcha_file = "src/examples/088636.png"
captcha_url = "https://rucaptcha.com/dist/web/99581b9d446a509a0a01954438a5e36a.jpg"


image_captcha = ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY)
result = image_captcha.captcha_handler(captcha_file=captcha_file)

print(result)

image_captcha = ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY)
result = image_captcha.captcha_handler(captcha_link=captcha_url)

print(result)


async def run():
    image_captcha = ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY)
    result = await image_captcha.aio_captcha_handler(captcha_file=captcha_file)
    print(result)

    image_captcha = ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY)
    result = await image_captcha.aio_captcha_handler(captcha_link=captcha_url)
    print(result)


asyncio.run(run())
