import asyncio

from python_rucaptcha.enums import GeetestEnm
from python_rucaptcha.GeeTest import GeeTest, aioGeeTest

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad9053f31111111755711108fa758111"

"""
Geetest example
"""

gt = GeeTest(
    rucaptcha_key=RUCAPTCHA_KEY,
    gt="f1ab2cdefa3456789012345b6c78d90e",
    method=GeetestEnm.GEETEST.value,
    pageurl="https://www.site.com/page/",
    api_server="api-na.geetest.com",
)

print(gt.captcha_handler(challenge="12345678abc90123d45678ef90123a456b"))


async def run():
    gt = aioGeeTest(
        rucaptcha_key=RUCAPTCHA_KEY,
        gt="f1ab2cdefa3456789012345b6c78d90e",
        method=GeetestEnm.GEETEST.value,
        pageurl="https://www.site.com/page/",
        api_server="api-na.geetest.com",
    )
    result = await gt.captcha_handler(challenge="12345678abc90123d45678ef90123a456b")
    print(result)


asyncio.run(run())

"""
Geetest 4 example
"""

gt = GeeTest(
    rucaptcha_key=RUCAPTCHA_KEY,
    method=GeetestEnm.GEETEST_V4.value,
    pageurl="https://www.site.com/page/",
    captcha_id="f1ab2cdefa3456789012345b6c78d90e",
    api_server="api-na.geetest.com",
)

print(gt.captcha_handler())


async def run():
    gt = aioGeeTest(
        rucaptcha_key=RUCAPTCHA_KEY,
        method=GeetestEnm.GEETEST_V4.value,
        pageurl="https://www.site.com/page/",
        captcha_id="f1ab2cdefa3456789012345b6c78d90e",
        api_server="api-na.geetest.com",
    )
    result = await gt.captcha_handler()
    print(result)


asyncio.run(run())
