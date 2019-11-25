import asyncio

import requests

from python_rucaptcha import RuCaptchaControl, KeyCaptcha, CallbackClient

"""
Этот пример показывает то как нужно работать с модулем для распознования KeyCaptcha - капчи пазла,
на примере нашего сайта.
В общем случае вам потребуется получение:
1. Получить данные капчи-пазла с сайта с этой капчёй.
Пример страницы для тестов - https://www.keycaptcha.com/signup/
Данные которые извлекаются с данной страницы и используются для дальнейшей работы:
s_s_c_user_id=15,
s_s_c_session_id='8f460599bebe02cb0dd096b1fe70b089',
s_s_c_web_server_sign ='edd2c221c05aece19f6db93a36b42272',
s_s_c_web_server_sign2 ='15989edaad1b4dc056ec8fa05abc7c9a',
page_url ='https://www.keycaptcha.com/signup/'

2. Передать извлечённые параметры в метод KeyCaptcha - captcha_handler(....)
"""
"""
В общем случаи запрос на решение капчи-пазла выглядит следующим способом
!!!Все параметры являются обязательными!!!
"""
RUCAPTCHA_KEY = "2597d7cb1f9435a3b531ac283ce987d5"


"""
contextmanager пример
"""

# синхронный пример contextmanager
with KeyCaptcha.KeyCaptcha(rucaptcha_key=RUCAPTCHA_KEY) as key_captcha:
    result = key_captcha.captcha_handler(
        key_params={
            "s_s_c_user_id": 15,
            "s_s_c_session_id": "8f460599bebe02cb0dd096b1fe70b089",
            "s_s_c_web_server_sign": "edd2c221c05aece19f6db93a36b42272",
            "s_s_c_web_server_sign2": "15989edaad1b4dc056ec8fa05abc7c9a",
            "pageurl": "https://www.keycaptcha.com/signup/",
        }
    )
    print(result)

# асинхронный пример contextmanager
async def aiocontext():
    with KeyCaptcha.aioKeyCaptcha(rucaptcha_key=RUCAPTCHA_KEY) as key_captcha:
        result = await key_captcha.captcha_handler(
            key_params={
                "s_s_c_user_id": 15,
                "s_s_c_session_id": "8f460599bebe02cb0dd096b1fe70b089",
                "s_s_c_web_server_sign": "edd2c221c05aece19f6db93a36b42272",
                "s_s_c_web_server_sign2": "15989edaad1b4dc056ec8fa05abc7c9a",
                "pageurl": "https://www.keycaptcha.com/signup/",
            }
        )
        print(result)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(aiocontext())
    loop.close()

answer = KeyCaptcha.KeyCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(
    key_params={
        "s_s_c_user_id": 15,
        "s_s_c_session_id": "8f460599bebe02cb0dd096b1fe70b089",
        "s_s_c_web_server_sign": "edd2c221c05aece19f6db93a36b42272",
        "s_s_c_web_server_sign2": "15989edaad1b4dc056ec8fa05abc7c9a",
        "pageurl": "https://www.keycaptcha.com/signup/",
    }
)

"""
answer - это JSON строка с соответствующими полями

user_answer_... - это JSON строка с соответствующими полями
captchaSolve - решение капчи,
taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
error - False - если всё хорошо, True - если есть ошибка,
errorBody - полная информация об ошибке: 
    {
        text - Развернётое пояснение ошибки
        id - уникальный номер ошибка в ЭТОЙ бибилотеке
    }
"""

# капча решена верно, ошибка = 0
if answer["error"] == 0:
    # решение капчи
    print(answer["captchaSolve"])
    print(answer["taskId"])
# во время решения капчи возникли ошибки, ошибка = 1
elif answer["error"] == 1:
    # Тело ошибки, если есть
    print(answer["errorBody"]["text"])
    print(answer["errorBody"]["id"])

"""
Пример асинхронного кода
"""


async def run():
    try:
        answer = await KeyCaptcha.aioKeyCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(
            key_params={
                "s_s_c_user_id": 15,
                "s_s_c_session_id": "8f460599bebe02cb0dd096b1fe70b089",
                "s_s_c_web_server_sign": "edd2c221c05aece19f6db93a36b42272",
                "s_s_c_web_server_sign2": "15989edaad1b4dc056ec8fa05abc7c9a",
                "pageurl": "https://www.keycaptcha.com/signup/",
            }
        )

        if not answer["error"]:
            # решение капчи
            print(answer["captchaSolve"])
            print(answer["taskId"])
        elif answer["error"]:
            # Тело ошибки, если есть
            print(answer["errorBody"]["text"])
            print(answer["errorBody"]["id"])
    except Exception as err:
        print(f"ERRRRORORO - {err}")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())
    loop.close()


"""
Callback пример
"""
# нужно передать IP/URL ранее зарегистрированного сервера
server_ip = "85.255.8.26"
# и по желанию - порт на сервере который слушает ваше веб-приложение
server_port = 8001
# регистрация нового домена для callback/pingback
answer = RuCaptchaControl.RuCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY).additional_methods(
    action="add_pingback", addr=f"http://{server_ip}:{server_port}/", json=1
)
print(answer)

# нужно придумать ЛЮБОЕ сложное название очереди(15+ знаков подойдёт)
queue_name = "ba86e77f9007_andrei_drang_7436e7_key_captcha_442674_cute_queue"
# регистрируем очередь на callback сервере
answer = requests.post(
    f"http://{server_ip}:{server_port}/register_key",
    json={"key": queue_name, "vhost": "rucaptcha_vhost"},
)

# если очередь зарегистрирована
if answer.text == "OK":
    # IP адрес должен быть ЗАРАНЕЕ зарегистрирован в системе (подробонсти смотри в `CaptchaTester/rucaptcha_control_example.py`)
    # создаём задание на сервере, ответ на которое придёт на заданный pingback URL в виде POST запроса
    task_creation_answer = KeyCaptcha.KeyCaptcha(
        rucaptcha_key=RUCAPTCHA_KEY,
        pingback=f"85.255.8.26:8001/rucaptcha/key_captcha/{queue_name}",
    ).captcha_handler(
        key_params={
            "s_s_c_user_id": 15,
            "s_s_c_session_id": "8f460599bebe02cb0dd096b1fe70b089",
            "s_s_c_web_server_sign": "edd2c221c05aece19f6db93a36b42272",
            "s_s_c_web_server_sign2": "15989edaad1b4dc056ec8fa05abc7c9a",
            "pageurl": "https://www.keycaptcha.com/signup/",
        }
    )
    print(task_creation_answer)

    # подключаемся к серверу и ждём решения капчи из кеша
    callback_server_response = CallbackClient.CallbackClient(
        task_id=task_creation_answer.get("id")
    ).captcha_handler()

    print(callback_server_response)

    # подключаемся к серверу и ждём решения капчи из RabbitMQ queue
    callback_server_response = CallbackClient.CallbackClient(
        task_id=task_creation_answer.get("id"), queue_name=queue_name, call_type="queue"
    ).captcha_handler()

    print(callback_server_response)
