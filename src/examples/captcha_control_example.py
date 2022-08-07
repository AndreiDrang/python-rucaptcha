import asyncio

from src.python_rucaptcha.enums import CaptchaControlEnm
from src.python_rucaptcha.CaptchaControl import CaptchaControl, aioCaptchaControl

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad911111111111ca81755768608fa758570"

# Balance control

control_captcha = CaptchaControl(rucaptcha_key=RUCAPTCHA_KEY, action=CaptchaControlEnm.GETBALANCE.value)
result = control_captcha.additional_methods()

print(result)

# Report control

control_captcha = CaptchaControl(rucaptcha_key=RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTBAD.value)
result = control_captcha.report(id="-1")

print(result)

control_captcha = CaptchaControl(rucaptcha_key=RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTGOOD.value)
result = control_captcha.report(id="-1")

print(result)

# Pingback control

control_captcha = CaptchaControl(rucaptcha_key=RUCAPTCHA_KEY, action=CaptchaControlEnm.DEL_PINGBACK.value)
result = control_captcha.domain_control(addr="all")

print(result)

# ASYNC


async def run():
    # Balance control

    control_captcha = aioCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY, action=CaptchaControlEnm.GETBALANCE.value)
    result = await control_captcha.additional_methods()

    print(result)

    # Report control

    control_captcha = aioCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTBAD.value)
    result = await control_captcha.report(id="-1")

    print(result)

    control_captcha = aioCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY, action=CaptchaControlEnm.REPORTGOOD.value)
    result = await control_captcha.report(id="-1")

    print(result)

    # Pingback control

    control_captcha = aioCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY, action=CaptchaControlEnm.DEL_PINGBACK.value)
    result = await control_captcha.domain_control(addr="all")

    print(result)


asyncio.run(run())
