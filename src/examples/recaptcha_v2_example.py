import requests
import CallbackClient

from python_rucaptcha import ReCaptchaV2, RuCaptchaControl

"""
UPDATE 2.4
Добавление возможности применять callback при получении ответа капчи
Для этого в класс нужно передать параметр `pingback` со значением URL'a для ожидания ответа, к примеру - 85.255.8.26/recaptcha_captcha
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
    
UPDATE 1.6.6
Добавление параметра для невидимой капчи - `invisible`(допустимые значения 1 и 0)
"""
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = ""
"""
Этот пример показывает работу модуля решения ReCaptcha v2 New
"""
# Google sitekey
SITE_KEY = "6Lf77CsUAAAAALLFD1wIhbfQRD07VxhvPbyQFaQJ"
# ссылка на страницу с капчёй
PAGE_URL = "https://pythoncaptcha.tech/"

# Пример работы с модулем ReCaptchaV2
answer_usual_re2 = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(
    site_key=SITE_KEY, page_url=PAGE_URL
)
print(answer_usual_re2)
"""
Этот пример показывает работу модуля решения Invisible ReCaptcha
"""

SITE_KEY = "6LcC7SsUAAAAAN3AOB-clPIsrKfnBUlO2QkC_vQ7"
PAGE_URL = "https://pythoncaptcha.tech/invisible_recaptcha/"

# Пример работы с модулем ReCaptchaV2
answer_invisible = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY, invisible=1).captcha_handler(
    site_key=SITE_KEY, page_url=PAGE_URL
)
print(answer_invisible)
"""
answer_... - это JSON строка с соответствующими полями

captchaSolve - решение капчи,
taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
error - False - если всё хорошо, True - если есть ошибка,
errorBody - полная информация об ошибке: 
	{
        text - Развернётое пояснение ошибки
        id - уникальный номер ошибка в ЭТОЙ бибилотеке
    }
"""
# обычная recaptcha v2
if not answer_usual_re2["error"]:
    # решение капчи
    print(answer_usual_re2["captchaSolve"])
    print(answer_usual_re2["taskId"])
elif answer_usual_re2["error"]:
    # Тело ошибки, если есть
    print(answer_usual_re2["errorBody"])

# invisible recaptcha v2
if not answer_invisible["error"]:
    # решение капчи
    print(answer_invisible["captchaSolve"])
    print(answer_invisible["taskId"])
elif answer_invisible["error"]:
    # Тело ошибки, если есть
    print(answer_invisible["errorBody"])


"""
Пример асинхронной работы 
"""
import asyncio


async def run():
    try:
        answer_aio_re2 = await ReCaptchaV2.aioReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(
            site_key=SITE_KEY, page_url=PAGE_URL
        )
        if not answer_aio_re2["error"]:
            # решение капчи
            print(answer_aio_re2["captchaSolve"])
            print(answer_aio_re2["taskId"])
        elif answer_aio_re2["error"]:
            # Тело ошибки, если есть
            print(answer_aio_re2["errorBody"])
            print(answer_aio_re2["errorBody"])
    except Exception as err:
        print(err)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
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
queue_name = "ba86e77f9007_andrei_drang_7436e7444060657442674_new_cute_queue"
# регистрируем очередь на callback сервере
answer = requests.post(
    f"http://{server_ip}:{server_port}/register_key",
    json={"key": queue_name, "vhost": "rucaptcha_vhost"},
)

# если очередь зарегистрирована
if answer.text == "OK":
    # IP адрес должен быть ЗАРАНЕЕ зарегистрирован в системе (подробонсти смотри в `CaptchaTester/rucaptcha_control_example.py`)
    # создаём задание на сервере, ответ на которое придёт на заданный pingback URL в виде POST запроса
    task_creation_answer = ReCaptchaV2.ReCaptchaV2(
        rucaptcha_key=RUCAPTCHA_KEY,
        pingback=f"pythoncaptcha.tech:8001/rucaptcha/recaptcha_captcha/{queue_name}",
    ).captcha_handler(site_key=SITE_KEY, page_url=PAGE_URL)

    print(task_creation_answer)

    # подключаемся к серверу и ждём решения капчи из кеша
    callback_server_response = CallbackClient.CallbackClient(task_id=task_creation_answer.get("id")).captcha_handler()

    print(callback_server_response)

    # подключаемся к серверу и ждём решения капчи из RabbitMQ queue
    callback_server_response = CallbackClient.CallbackClient(
        task_id=task_creation_answer.get("id"), queue_name=queue_name, call_type="queue"
    ).captcha_handler()

    print(callback_server_response)
