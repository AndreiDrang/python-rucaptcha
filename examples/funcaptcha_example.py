# v.2.4
import asyncio

import requests

from python_rucaptcha import FunCaptcha, RuCaptchaControl, CallbackClient

"""
Данный пример показывает работу модуля с FunCaptcha
"""

"""
UPDATE 2.4
Добавление возможности применять callback при получении ответа капчи
Для этого в класс нужно передать параметр `pingback` со значением URL'a для ожидания ответа, к примеру - 85.255.8.26/fun_captcha
Полный пример работы приведён в самом низу документа
Пример сервера принимающего POST запросы от RuCaptcha находится в - `CaptchaTester/callback_examples/callback_server.py`

UPDATE 2.0
Переработка JSON-ответа пользователю(раздела с ошибками), новый ответ:
    {
        captchaSolve - решение капчи,
        taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
        error - False - если ошибок нет, True - если есть ошибка,
        errorBody - полная информация об ошибке: 
            {
                text - Развернётое пояснение ошибки
                id - уникальный номер ошибка в ЭТОЙ бибилотеке
            }
    }
"""
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = "aafb515dff0075f94b1f3328615bc0fd"

"""
Страница на которой находится FunCaptch: 
https://www.funcaptcha.com/demo
Данные взятые из этой страницы о данной капче:
"""
public_key = "DE0B0BB7-1EE4-4D70-1853-31B835D4506B"
pageurl = "https://www.funcaptcha.com/demo"

"""
contextmanager пример
"""

# синхронный пример contextmanager
with FunCaptcha.FunCaptcha(rucaptcha_key=RUCAPTCHA_KEY) as fun_captcha:
    result = fun_captcha.captcha_handler(public_key=public_key, page_url=pageurl)
    print(result)

# асинхронный пример contextmanager
async def aiocontext():
    with FunCaptcha.aioFunCaptcha(rucaptcha_key=RUCAPTCHA_KEY) as fun_captcha:
        result = await fun_captcha.captcha_handler(public_key=public_key, page_url=pageurl)
        print(result)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(aiocontext())
    loop.close()

"""
Обычный пример для решения FunCaptcha
"""
answer = FunCaptcha.FunCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(
    public_key=public_key, page_url=pageurl
)

"""
answer - это JSON строка с соответствующими полями
captchaSolve - решение капчи,
taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
error - False - если всё хорошо, True - если есть ошибка,
errorBody - полная информация об ошибке: 
    {
        text - Развернётое пояснение ошибки
        id - уникальный номер ошибка в ЭТОЙ бибилотеке
    }
"""

if not answer["error"]:
    # решение капчи
    print(answer["captchaSolve"])
    print(answer["taskId"])
elif answer["error"]:
    # Тело ошибки, если есть
    print(answer["errorBody"])


"""
Пример асинхронного кода
"""


async def run():
    try:
        answer = await FunCaptcha.aioFunCaptcha(rucaptcha_key="RUCAPTCHA_KEY").captcha_handler(
            public_key=public_key, page_url=pageurl
        )
        if not answer["error"]:
            # решение капчи
            print(answer["captchaSolve"])
            print(answer["taskId"])
        elif answer["error"]:
            # Тело ошибки, если есть
            print(answer["errorBody"])
    except Exception as err:
        print(err)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())
    loop.close()

"""
Callback пример
"""
# нужно передать IP/URL ранее зарегистрированного сервера
server_ip = "pythoncaptcha.tech"
# и по желанию - порт на сервере который слушает ваше веб-приложение
server_port = 8001
# регистрация нового домена для callback/pingback
answer = RuCaptchaControl.RuCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY).additional_methods(
    action="add_pingback", addr=f"http://{server_ip}:{server_port}/", json=1
)
print(answer)

# нужно придумать ЛЮБОЕ сложное название очереди(15+ знаков подойдёт)
queue_name = "ba86e77f9007_andrei_drang_7436e7444060657442674_cute_queue"
# регистрируем очередь на callback сервере
answer = requests.post(
    f"http://{server_ip}:{server_port}/register_key",
    json={"key": queue_name, "vhost": "rucaptcha_vhost"},
)

# если очередь зарегистрирована
if answer.text == "OK":
    # IP адрес должен быть ЗАРАНЕЕ зарегистрирован в системе (подробонсти смотри в `CaptchaTester/rucaptcha_control_example.py`)
    # создаём задание на сервере, ответ на которое придёт на заданный pingback URL в виде POST запроса
    task_creation_answer = FunCaptcha.FunCaptcha(
        rucaptcha_key=RUCAPTCHA_KEY,
        pingback=f"pythoncaptcha.tech:8001/rucaptcha/fun_captcha/{queue_name}",
    ).captcha_handler(public_key=public_key, page_url=pageurl)

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
