from python_rucaptcha import ReCaptchaV3

"""
UPDATE 2.5
Добавление возможности решать капчу ReCaptcha V3
"""
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = ""
"""
Этот пример показывает работу модуля решения ReCaptcha V3

Подробней: https://rucaptcha.com/api-rucaptcha#solving_recaptchav3
"""
# Google sitekey
SITE_KEY = "6Lf77CsUAAAAALLFD1wIhbfQRD07VxhvPbyQFaQJ"
# ссылка на страницу с капчёй
PAGE_URL = "https://pythoncaptcha.tech/"
# Значение параметра action, которые вы нашли в коде сайта
ACTION = "verify"
# Требуемое значение рейтинга (score) работника, от 0.1(робот) до 0.9(человечный человек)
MIN_SCORE = 0.4

# Пример работы с модулем ReCaptchaV3, передача минимального количества параметров
answer_usual_re3 = ReCaptchaV3.ReCaptchaV3(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(
    site_key=SITE_KEY, page_url=PAGE_URL
)
print(answer_usual_re3)

# Пример работы с модулем ReCaptchaV3, передача всех основных параметров параметров
answer_usual_re3_f = ReCaptchaV3.ReCaptchaV3(
    rucaptcha_key=RUCAPTCHA_KEY, action=ACTION, min_score=MIN_SCORE
).captcha_handler(site_key=SITE_KEY, page_url=PAGE_URL)
print(answer_usual_re3_f)
"""
answer_... - это JSON строка с соответствующими полями

captchaSolve - решение капчи,
user_check - ID работника, который решил капчу,
user_score -  score решившего капчу работника,
taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
error - False - если всё хорошо, True - если есть ошибка,
errorBody - полная информация об ошибке:
	{
        text - Развернётое пояснение ошибки
        id - уникальный номер ошибка в ЭТОЙ бибилотеке
    }
"""
# обычная recaptcha v3
if not answer_usual_re3["error"]:
    # решение капчи
    print(answer_usual_re3["captchaSolve"])
    print(answer_usual_re3["taskId"])
    print(answer_usual_re3["user_check"])
    print(answer_usual_re3["user_score"])
elif answer_usual_re3["error"]:
    # Тело ошибки, если есть
    print(answer_usual_re3["errorBody"])

# обычная recaptcha v3
if not answer_usual_re3_f["error"]:
    # решение капчи
    print(answer_usual_re3_f["captchaSolve"])
    print(answer_usual_re3_f["taskId"])
    print(answer_usual_re3["user_check"])
    print(answer_usual_re3["user_score"])
elif answer_usual_re3_f["error"]:
    # Тело ошибки, если есть
    print(answer_usual_re3_f["errorBody"])

"""
Пример асинхронной работы 

Паарметры для синхронной и асинхронной работы - идентичны
"""
import asyncio


async def run():
    try:
        answer_aio_re3 = await ReCaptchaV3.aioReCaptchaV3(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(
            site_key=SITE_KEY, page_url=PAGE_URL
        )
        if not answer_aio_re3["error"]:
            # решение капчи
            print(answer_aio_re3["captchaSolve"])
            print(answer_aio_re3["taskId"])
            print(answer_aio_re3["user_check"])
            print(answer_aio_re3["user_score"])
        elif answer_aio_re3["error"]:
            # Тело ошибки, если есть
            print(answer_aio_re3["errorBody"])
    except Exception as err:
        print(err)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
