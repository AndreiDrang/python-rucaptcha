import asyncio
from python_rucaptcha.CapyPuzzle import CapyPuzzle, aioCapyPuzzle

"""
Синхронный пример решения капчи
"""
capy = CapyPuzzle(rucaptcha_key="2bfbe92f00f1498e90e1460550b1ad94")
result = capy.captcha_handler(
    captchakey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
    page_url="https://www.capy.me/account/register/",
)

if not result["error"]:
    # решение капчи
    print(result["captchaSolve"])
    print(result["taskId"])
elif result["error"]:
    # Тело ошибки, если есть
    print(result["errorBody"])


async def run():
    try:
        result = await aioCapyPuzzle(rucaptcha_key="2bfbe92f00f1498e90e1460550b1ad94").captcha_handler(
            captchakey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w",
            page_url="https://www.capy.me/account/register/",
        )
        if not result["error"]:
            # решение капчи
            print(result["captchaSolve"])
            print(result["taskId"])
        elif result["error"]:
            # Тело ошибки, если есть
            print(result["errorBody"])
    except Exception as err:
        print(err)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())
    loop.close()
