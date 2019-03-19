import asyncio
import time
import random

import aiohttp

"""
Задаётся IP/URL на котором запущен сервер и порт
YOUR_HOST_OR_IP:PORT
"""
# IP для работы callback`a
HOST = "85.255.8.26"
# PORT для работы callback`a
PORT = 8001

QUEUE_KEY = "ba86e77f9007a106c2eb2d7436e7444060657442674"
TASK_ID = "60657442675"


async def send_solvings(route: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"http://{HOST}:{PORT}/rucaptcha/{route}/{QUEUE_KEY}",
            data={"id": TASK_ID, "code": "088636"},
        ) as resp:
            await resp.read()


def main():
    routes = (
        "fun_captcha",
        "image_captcha",
        "key_captcha",
        "media_captcha",
        "recaptcha_captcha",
        "rotate_captcha",
    )
    while True:
        loop = asyncio.new_event_loop()

        tasks = [send_solvings(random.choice(routes)) for i in range(2)]

        print("GOOOO!!!...")
        start_time = time.time()

        # запускаем эмулятор сервера РуКапчи
        loop.run_until_complete(asyncio.wait(tasks))

        loop.close()
        end_time = time.time()

        print(
            f"""
                  Loops - {len(tasks)};
                  Whole time - {round(end_time-start_time, 4)};
                  Time per request - {round((end_time-start_time)/len(tasks), 5)};
               """
        )

        print("STOOOOP!!!...\n")
        time.sleep(2)


main()
