# v.1.0.a
from python_rucaptcha import TextCaptcha


"""
Этот пример показывает то как нужно работать с модулем для решения текстовых капч
"""
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = ''
# Пример вопроса для решения
text_question = 'Если завтра суббота, то какой сегодня день?'
"""
Тут нужно воспользоваться бибилотекой, отослать на решение ссылку на капчу и получить ответ
далее его записать в user_answer и отправить на проверку уже на наш сайт


Первый пример демонстрирует сохранеие файла изображения как обычного файла в папу
"""
user_answer = TextCaptcha.TextCaptcha(rucaptcha_key = RUCAPTCHA_KEY).captcha_handler(captcha_text = text_question)

'''
user_answer_... - это JSON строка с соответствующими полями

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

if user_answer['errorId'] == 0:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
elif user_answer['errorId'] == 1:
	# Тело ошибки, если есть
	print(user_answer['errorBody'])

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

if user_answer_full['errorId'] == 0:
	# решение капчи
	print(user_answer_full['captchaSolve'])
	print(user_answer_full['taskId'])
elif user_answer_full['errorId'] == 1:
	# Тело ошибки, если есть
	print(user_answer_full['errorBody'])