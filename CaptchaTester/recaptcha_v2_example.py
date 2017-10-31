from python_rucaptcha import ReCaptchaV2


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

"""
Этот пример показывает работу модуля решения Invisible ReCaptcha
"""

SITE_KEY = '6LcC7SsUAAAAAN3AOB-clPIsrKfnBUlO2QkC_vQ7'
PAGE_URL = 'http://85.255.8.26/invisible_recaptcha/'

# Пример работы с модулем ReCaptchaV2
answer_invisible = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY,
                                                                                        page_url=PAGE_URL)
'''
answer_... - это JSON строка с соответствующими полями

captchaSolve - решение капчи,
taskId - находится Id задачи на решение капчи,
errorId - 0 - если всё хорошо, 1 - если есть ошибка,
errorBody - тело ошибки, если есть.
{
    "captchaSolve": string,
    "taskId": int,
    "errorId": int, 1 or 0,
    "errorBody": string,
}
'''
# обычная recaptcha v2
if answer_usual_re2['errorId'] == 0:
	# решение капчи
	print(answer_usual_re2['captchaSolve'])
	print(answer_usual_re2['taskId'])
elif answer_usual_re2['errorId'] == 1:
	# Тело ошибки, если есть
	print(answer_usual_re2['errorBody'])

# invisible recaptcha v2
if answer_invisible['errorId'] == 0:
	# решение капчи
	print(answer_invisible['captchaSolve'])
	print(answer_invisible['taskId'])
elif answer_invisible['errorId'] == 1:
	# Тело ошибки, если есть
	print(answer_invisible['errorBody'])

"""
Пример асинхронной работы 
"""
import asyncio


async def run():
	try:
		answer_aio_re2 = await ReCaptchaV2.aioReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY,
																									   page_url=PAGE_URL)
		if answer_aio_re2['errorId'] == 0:
			# решение капчи
			print(answer_aio_re2['captchaSolve'])
			print(answer_aio_re2['taskId'])
		elif answer_aio_re2['errorId'] == 1:
			# Тело ошибки, если есть
			print(answer_aio_re2['errorBody'])
	except Exception as err:
		print(err)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run())
	loop.close()
