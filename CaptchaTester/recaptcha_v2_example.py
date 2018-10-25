from python_rucaptcha import ReCaptchaV2

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
RUCAPTCHA_KEY = ""
"""
Этот пример показывает работу модуля решения ReCaptcha v2 New
"""
# Введите ключ от рукапчи из своего аккаунта
SITE_KEY = '6Lf77CsUAAAAALLFD1wIhbfQRD07VxhvPbyQFaQJ'
PAGE_URL = 'http://85.255.8.26/'

# Пример работы с модулем ReCaptchaV2
answer_usual_re2 = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY,
                                                                                        page_url=PAGE_URL)
print(answer_usual_re2)
"""
Этот пример показывает работу модуля решения Invisible ReCaptcha
"""

SITE_KEY = '6LcC7SsUAAAAAN3AOB-clPIsrKfnBUlO2QkC_vQ7'
PAGE_URL = 'http://85.255.8.26/invisible_recaptcha/'

# Пример работы с модулем ReCaptchaV2
answer_invisible = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY, invisible=1).captcha_handler(site_key=SITE_KEY,
																									 page_url=PAGE_URL)
print(answer_invisible)
'''
answer_... - это JSON строка с соответствующими полями

captchaSolve - решение капчи,
taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
error - False - если всё хорошо, True - если есть ошибка,
errorBody - полная информация об ошибке: 
	{
        text - Развернётое пояснение ошибки
        id - уникальный номер ошибка в ЭТОЙ бибилотеке
    }
'''
# обычная recaptcha v2
if not answer_usual_re2['error']:
	# решение капчи
	print(answer_usual_re2['captchaSolve'])
	print(answer_usual_re2['taskId'])
elif answer_usual_re2['error']:
	# Тело ошибки, если есть
	print(answer_usual_re2['errorBody']['text'])
	print(answer_usual_re2['errorBody']['id'])

# invisible recaptcha v2
if not answer_invisible['error']:
	# решение капчи
	print(answer_invisible['captchaSolve'])
	print(answer_invisible['taskId'])
elif answer_invisible['error']:
	# Тело ошибки, если есть
	print(answer_invisible['errorBody']['text'])
	print(answer_invisible['errorBody']['id'])


"""
Пример асинхронной работы 
"""
import asyncio


async def run():
	try:
		answer_aio_re2 = await ReCaptchaV2.aioReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY,
																									   page_url=PAGE_URL)
		if not answer_aio_re2['error']:
			# решение капчи
			print(answer_aio_re2['captchaSolve'])
			print(answer_aio_re2['taskId'])
		elif answer_aio_re2['error']:
			# Тело ошибки, если есть
			print(answer_aio_re2['errorBody']['text'])
			print(answer_aio_re2['errorBody']['id'])
	except Exception as err:
		print(err)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run())
	loop.close()

"""
Callback пример
"""
# IP адрес должен быть ЗАРАНЕЕ зарегистрирован в системе (подробонсти смотри в `CaptchaTester/rucaptcha_control_example.py`)
# создаём задание на сервере, ответ на которое придёт на заданный pingback URL в виде POST запроса
callback_answer = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY, 
                                          pingback='85.255.8.26/recaptcha_captcha', 
                                         ).captcha_handler(site_key=SITE_KEY,
											 			   page_url=PAGE_URL)
print(callback_answer)