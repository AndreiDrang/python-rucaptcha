from python_rucaptcha import TextCaptcha


"""
Этот пример показывает то как нужно работать с модулем для решения текстовых капч
"""

'''
UPDATE 2.4
Добавление возможности применять callback при получении ответа капчи
Для этого в класс нужно передать параметр `pingback` со значением URL'a для ожидания ответа, к примеру - 85.255.8.26/text_captcha
Полный пример работы приведён в самом низу документа
Пример сервера принимающего POST запросы от RuCaptcha находится в - `CaptchaTester/callback_examples/callback_server.py`

UPDATE 2.0
user_answer_... - это JSON строка с соответствующими полями

captchaSolve - решение капчи,
taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
error - False - если всё хорошо, True - если есть ошибка,
errorBody - полная информация об ошибке: 
    {
        text - Развернётое пояснение ошибки
        id - уникальный номер ошибка в ЭТОЙ бибилотеке
    }
'''
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = 'ba86e77f9007a106c2eb2d7436e74440'
# Пример вопроса для решения
text_question = 'Если завтра суббота, то какой сегодня день?'
"""
Тут нужно воспользоваться бибилотекой, отослать на решение ссылку на капчу и получить ответ
далее его записать в user_answer
"""
user_answer = TextCaptcha.TextCaptcha(rucaptcha_key = RUCAPTCHA_KEY).captcha_handler(captcha_text = text_question)

if user_answer['error'] == 0:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
elif user_answer['error'] == 1:
	# Тело ошибки, если есть
	print(user_answer['errorBody']['text'])
	print(user_answer['errorBody']['id'])

'''
Так же класс в качестве параметра может принимать список необязательных переменных, таких как:
language = 0,1,2
и прочие.

Все параметры
https://rucaptcha.com/api-rucaptcha#solving_text_captcha

Полный пример выглядит так:
'''
user_answer_full = TextCaptcha.TextCaptcha(rucaptcha_key = RUCAPTCHA_KEY,
                                           language = 1).captcha_handler(captcha_text = text_question)

if user_answer_full['error'] == 0:
	# решение капчи
	print(user_answer_full['captchaSolve'])
	print(user_answer_full['taskId'])
elif user_answer_full['error'] == 1:
	# Тело ошибки, если есть
	print(user_answer_full['errorBody']['text'])
	print(user_answer_full['errorBody']['id'])

"""
Callback пример
"""
# IP адрес должен быть ЗАРАНЕЕ зарегистрирован в системе (подробонсти смотри в `CaptchaTester/rucaptcha_control_example.py`)
# создаём задание на сервере, ответ на которое придёт на заданный pingback URL в виде POST запроса
callback_answer = TextCaptcha.TextCaptcha(rucaptcha_key=RUCAPTCHA_KEY, 
										  pingback='85.255.8.26/text_captcha',
                                          language = 1 
                                         ).captcha_handler(captcha_text = text_question)

print(callback_answer)