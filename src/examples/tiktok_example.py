import asyncio

from src.python_rucaptcha.enums import TikTokCaptchaEnm
from src.python_rucaptcha.TikTokCaptcha import TikTokCaptcha, aioTikTokCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad9053f111111111111111fa758570"

pageurl = "https://www.tiktok.com/login/phone-or-email/email"
aid = "1459"
host = "https://www-useast1a.tiktok.com"
cookies = """tt_csrf_token=8TwpFXMK-xelhfHWNk3vCmOMS_IywmgR76J0; _abck=8C88FA5F886F14E362F71367E51C4A9E~-1~YAAQjHcRJX90XWqCAQAA741ldQgF9RvxGZfIEjhEFlVUSExtmO4pX+v3KcL4MDHYTdUnHP5y+auSOIIqFVMAhfKhu0OglashmiyFuGaRCbjoAKcSq18ov43zc4xIGnOIh2njJYLO8XTTK4NAUPzQsv90nNTiC4sJ8J28WJcD8rWiJohPmtVi++J2hkWuNrq4kfVHifiw0a6J11rPUgzoY0sYId9L3b7bEGlYidstBEVkxsdIakysU7WPRPQuXQ5ORX1y9VRI1/S8SRJCPT8hsw5VGnA3ZTWoos+U2QNe6jOmh+r2lVGQp26d1NuK4j4KeexEGwwIRC3NbMPnoM7svr7Ah5/ZgTbRdqrfr0TxYNtD+BQJ/BZvEtHQ0g==~-1~-1~-1; ak_bmsc=0C59B98852D34B6024F09565AEF3DABF~000000000000000000000000000000~YAAQjHcRJYB0XWqCAQAA741ldRAyqwRUurqvl1ooYUAfu4RlKyAekfk9EdU+PnOOEzfrYTH4vBiM5Tyu53PXzOFxSv+6Mmr/eS525r8YKkC4OlBSXNEKp49lcOeEir0EZc5FDSa1GsdGTOeqds7kEtGeAoGYOfbaFqebrqcgXIFm6bruPiaQSIa71ibE0RWEylGZUqEm9XidFgHi7owbbDfnFIHjAkY9OIBXtCyysN6f2LnjA77U6Iz8Vc+ZnnCy7EpU27zBp9g8gHc6XlsWgVZczCkI2sAyvLNyhNdNvr66DFXQGPooUVFt1eu7Wr84hyeqkVIZ/e6JeO7eeWD3m3BJdhSLFH9cG8Inu+ucssezA0HGBWRLLsuvtQcouMbyiC0/QMhAfy2ZEw==; bm_sz=2D2B267FF82108C34A71921FDD3E4210~YAAQjHcRJYJ0XWqCAQAA741ldRA3VZyY/6SSndh905A0t2BxLX6h2sT3tz6/c3OetEbNcLssuaKjLmUUBjCsMqknZi/wN8Ak90SsKwDcOxrRrVIbsiG1mvfU2XAkrCe+l9iBIi5PdoSje6KzSXfW975Ozpz6dADDiT+KRHaQV4S/HdmjZf4U8AH0JzZe2LvkB1Wuq/HOUVsP7HVY37MPf9RvRjCKvXG8JO5lZ6e3AZtn+Gb8CITDkOQb9Sf1HlFYFMt3PiwG6Rs1L7jiSaDIfqTUJcId0ho038whNTw4e0UPmLs=~4474177~3753529; __tea_cache_tokens_1988={"_type_":"default","user_unique_id":"7128902427751990789","timestamp":1659826966712}; ttwid=1|oK5Qviu6-AtiV6tRgdrXlMWI53OUuO9saqvbF-oeiK8|1659826966|21b12ceb761e86e9047915dc0ac9408df142065490e46ef5d28c92ba67c7593e; msToken=u4oKalLxmidukiJRtA0mRHvZtHc3xEbPiTstK6IsUUF_a1I4N94cB6OComtfBmmIdabLxfLi_eVSRGGW3_k3x2KlKqIp3XG04NEfrTyOl9URRszHOpX3; msToken=u4oKalLxmidukiJRtA0mRHvZtHc3xEbPiTstK6IsUUF_a1I4N94cB6OComtfBmmIdabLxfLi_eVSRGGW3_k3x2KlKqIp3XG04NEfrTyOl9URRszHOpX3"""


tiktok_captcha = TikTokCaptcha(
    rucaptcha_key=RUCAPTCHA_KEY,
    method=TikTokCaptchaEnm.TIKTOK.value,
    pageurl=pageurl,
    aid=aid,
    host=host,
    cookies=cookies,
)
result = tiktok_captcha.captcha_handler()

print(result)

# ASYNC


async def run():
    # Balance control

    tiktok_captcha = aioTikTokCaptcha(
        rucaptcha_key=RUCAPTCHA_KEY,
        method=TikTokCaptchaEnm.TIKTOK.value,
        pageurl=pageurl,
        aid=aid,
        host=host,
        cookies=cookies,
    )
    result = await tiktok_captcha.captcha_handler()

    print(result)


asyncio.run(run())
