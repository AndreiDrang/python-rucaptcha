import asyncio

from src.python_rucaptcha.ImageCaptcha import ImageCaptcha, aioImageCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad911111111111ca81755768608fa758570"

captcha_file = "src/examples/088636.png"
captcha_url = "https://pythoncaptcha.xyz/static/image/common_image_example/862963.png"


image_captcha = ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY)
result = image_captcha.captcha_handler(captcha_file=captcha_file)

print(result)

image_captcha = ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY)
result = image_captcha.captcha_handler(captcha_link=captcha_url)

print(result)


async def run():
    image_captcha = aioImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY)
    result = await image_captcha.captcha_handler(captcha_file=captcha_file)
    print(result)

    image_captcha = aioImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY)
    result = await image_captcha.captcha_handler(captcha_link=captcha_url)
    print(result)


asyncio.run(run())
