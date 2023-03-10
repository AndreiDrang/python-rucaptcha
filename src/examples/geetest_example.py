import asyncio

from python_rucaptcha.core.enums import GeetestEnm
from python_rucaptcha.gee_test import GeeTest

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad9053f31111a8171111111111a758570"

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
    gt = GeeTest(
        rucaptcha_key=RUCAPTCHA_KEY,
        gt="f1ab2cdefa3456789012345b6c78d90e",
        method=GeetestEnm.GEETEST.value,
        pageurl="https://www.site.com/page/",
        api_server="api-na.geetest.com",
    )
    result = await gt.aio_captcha_handler(challenge="12345678abc90123d45678ef90123a456b")
    print(result)


asyncio.run(run())

"""
Geetest 4 example
"""

gt = GeeTest(
    rucaptcha_key=RUCAPTCHA_KEY,
    method=GeetestEnm.GEETEST_V4.value,
    pageurl="https://rucaptcha.com/demo/geetest-v4",
    captcha_id="e392e1d7fd421dc63325744d5a2b9c73",
)

print(gt.captcha_handler())


async def run():
    gt = GeeTest(
        rucaptcha_key=RUCAPTCHA_KEY,
        method=GeetestEnm.GEETEST_V4.value,
        pageurl="https://rucaptcha.com/demo/geetest-v4",
        captcha_id="e392e1d7fd421dc63325744d5a2b9c73",
    )
    result = await gt.aio_captcha_handler()
    print(result)


asyncio.run(run())
