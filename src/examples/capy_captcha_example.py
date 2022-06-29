import asyncio

from python_rucaptcha.CapyPuzzle import CapyPuzzle, aioCapyPuzzle


capy = CapyPuzzle(
    rucaptcha_key="2bfbe92f00f1498e90e1460550b1ad94",
    captchakey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
    pageurl="https://www.capy.me/account/register/",
)
result = capy.captcha_handler()

print(result)


async def run():
    try:
        result = await aioCapyPuzzle(
            rucaptcha_key="2bfbe92f00f1498e90e1460550b1ad94",
            captchakey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            pageurl="https://www.capy.me/account/register/",
        ).captcha_handler()
        print(result)
    except Exception as err:
        print(err)


asyncio.run(run())
