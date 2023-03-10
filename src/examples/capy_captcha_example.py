import asyncio

from python_rucaptcha.capy_puzzle import CapyPuzzle
from python_rucaptcha.core.enums import CapyPuzzleEnm

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad911111111111ca81755768608fa758570"

captchakey = "PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w"
pageurl = "https://www.capy.me/account/register/"
api_server = "https://jp.api.capy.me/"
versions = ["puzzle", "avatar"]

capy = CapyPuzzle(
    rucaptcha_key=RUCAPTCHA_KEY,
    captchakey=captchakey,
    pageurl=pageurl,
    method=CapyPuzzleEnm.CAPY.value,
    api_server=api_server,
    version=versions[0],
)
result = capy.captcha_handler()

print(result)


async def run():
    try:
        result = await CapyPuzzle(
            rucaptcha_key=RUCAPTCHA_KEY,
            captchakey=captchakey,
            pageurl=pageurl,
            method=CapyPuzzleEnm.CAPY.value,
            api_server=api_server,
            version=versions[0],
        ).aio_captcha_handler()
        print(result)
    except Exception as err:
        print(err)


asyncio.run(run())
