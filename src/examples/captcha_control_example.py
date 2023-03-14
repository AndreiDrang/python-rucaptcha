import asyncio

from python_rucaptcha.control import Control
from python_rucaptcha.core.enums import ControlEnm

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad911111111111ca81755768608fa758570"

# Balance control

control_captcha = Control(rucaptcha_key=RUCAPTCHA_KEY, action=ControlEnm.GETBALANCE.value)
result = control_captcha.additional_methods()

print(result)

# Report control

control_captcha = Control(rucaptcha_key=RUCAPTCHA_KEY, action=ControlEnm.REPORTBAD.value)
result = control_captcha.report(id="-1")

print(result)

control_captcha = Control(rucaptcha_key=RUCAPTCHA_KEY, action=ControlEnm.REPORTGOOD.value)
result = control_captcha.report(id="-1")

print(result)

# Pingback control

control_captcha = Control(rucaptcha_key=RUCAPTCHA_KEY, action=ControlEnm.DEL_PINGBACK.value)
result = control_captcha.domain_control(addr="all")

print(result)

# ASYNC


async def run():
    # Balance control

    control_captcha = Control(rucaptcha_key=RUCAPTCHA_KEY, action=ControlEnm.GETBALANCE.value)
    result = await control_captcha.aio_additional_methods()

    print(result)

    # Report control

    control_captcha = Control(rucaptcha_key=RUCAPTCHA_KEY, action=ControlEnm.REPORTBAD.value)
    result = await control_captcha.aio_report(id="-1")

    print(result)

    control_captcha = Control(rucaptcha_key=RUCAPTCHA_KEY, action=ControlEnm.REPORTGOOD.value)
    result = await control_captcha.aio_report(id="-1")

    print(result)

    # Pingback control

    control_captcha = Control(rucaptcha_key=RUCAPTCHA_KEY, action=ControlEnm.DEL_PINGBACK.value)
    result = await control_captcha.aio_domain_control(addr="all")

    print(result)


asyncio.run(run())
