import requests

from python_rucaptcha import ReCaptchaV3, RuCaptchaControl, CallbackClient

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
SITE_KEY = '6Lf77CsUAAAAALLFD1wIhbfQRD07VxhvPbyQFaQJ'
# ссылка на страницу с капчёй
PAGE_URL = 'http://85.255.8.26/'
# Значение параметра action, которые вы нашли в коде сайта
ACTION = 'verify'
# Требуемое значение рейтинга (score) работника, от 0.1(робот) до 0.9(человечный человек)
MIN_SCORE = 0.4

# Пример работы с модулем ReCaptchaV3, передача минимального количества параметров
answer_usual_re3 = ReCaptchaV3.ReCaptchaV3(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY,
                                                                                        page_url=PAGE_URL)
print(answer_usual_re3)

# Пример работы с модулем ReCaptchaV3, передача всех основных параметров параметров
answer_usual_re3_f = ReCaptchaV3.ReCaptchaV3(rucaptcha_key=RUCAPTCHA_KEY,
										   action = ACTION, 
										   min_score = MIN_SCORE).captcha_handler(site_key=SITE_KEY,
										   										  page_url=PAGE_URL)
print(answer_usual_re3_f)
'''
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
'''
# обычная recaptcha v3
if not answer_usual_re3['error']:
	# решение капчи
	print(answer_usual_re3['captchaSolve'])
	print(answer_usual_re3['taskId'])
	print(answer_usual_re3['user_check'])
	print(answer_usual_re3['user_score'])
elif answer_usual_re3['error']:
	# Тело ошибки, если есть
	print(answer_usual_re3['errorBody']['text'])
	print(answer_usual_re3['errorBody']['id'])

# обычная recaptcha v3
if not answer_usual_re3_f['error']:
	# решение капчи
	print(answer_usual_re3_f['captchaSolve'])
	print(answer_usual_re3_f['taskId'])
	print(answer_usual_re3['user_check'])
	print(answer_usual_re3['user_score'])
elif answer_usual_re3_f['error']:
	# Тело ошибки, если есть
	print(answer_usual_re3_f['errorBody']['text'])
	print(answer_usual_re3_f['errorBody']['id'])

"""
Пример асинхронной работы 

Паарметры для синхронной и асинхронной работы - идентичны
"""
import asyncio


async def run():
	try:
		answer_aio_re3 = await ReCaptchaV3.aioReCaptchaV3(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY,
																									   page_url=PAGE_URL)
		if not answer_aio_re3['error']:
			# решение капчи
			print(answer_aio_re3['captchaSolve'])
			print(answer_aio_re3['taskId'])
			print(answer_aio_re3['user_check'])
			print(answer_aio_re3['user_score'])
		elif answer_aio_re3['error']:
			# Тело ошибки, если есть
			print(answer_aio_re3['errorBody']['text'])
			print(answer_aio_re3['errorBody']['id'])
	except Exception as err:
		print(err)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run())
	loop.close()

"""
Callback пример

***
Coming soon
***
"""
'''
# нужно передать IP/URL ранее зарегистрированного сервера
server_ip = '85.255.8.26'
# и по желанию - порт на сервере который слушает ваше веб-приложение
server_port = 8001
# регистрация нового домена для callback/pingback
answer = RuCaptchaControl.RuCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY).additional_methods(action='add_pingback', addr=f'http://{server_ip}:{server_port}/', json=1)
print(answer)

# нужно придумать ЛЮБОЕ сложное название очереди(15+ знаков подойдёт)
queue_name = 'ba86e77f9007_andrei_drang_7436e7444060657442674_new_cute_queue'
# регистрируем очередь на callback сервере
answer = requests.post(f'http://{server_ip}:{server_port}/register_key', json={'key':queue_name, 'vhost': 'rucaptcha_vhost'})

# если очередь зарегистрирована
if answer.text == 'OK':
    # IP адрес должен быть ЗАРАНЕЕ зарегистрирован в системе (подробонсти смотри в `CaptchaTester/rucaptcha_control_example.py`)
    # создаём задание на сервере, ответ на которое придёт на заданный pingback URL в виде POST запроса
    task_creation_answer = ReCaptchaV3.ReCaptchaV3(rucaptcha_key=RUCAPTCHA_KEY, 
                                          pingback=f'85.255.8.26:8001/rucaptcha/recaptcha_captcha/{queue_name}', 
                                         ).captcha_handler(site_key=SITE_KEY,
											 			   page_url=PAGE_URL)

    print(task_creation_answer)

    # подключаемся к серверу и ждём решения капчи из кеша
    callback_server_response = CallbackClient.CallbackClient(task_id=task_creation_answer.get('id')).captcha_handler()

    print(callback_server_response)

    # подключаемся к серверу и ждём решения капчи из RabbitMQ queue
    callback_server_response = CallbackClient.CallbackClient(task_id=task_creation_answer.get('id'), queue_name=queue_name, call_type='queue').captcha_handler()

    print(callback_server_response)
'''