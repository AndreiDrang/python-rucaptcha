# v.1.6.2
from python_rucaptcha import KeyCaptcha

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
RUCAPTCHA_KEY = ''

answer = KeyCaptcha.KeyCaptcha(rucaptcha_key=RUCAPTCHA_KEY) \
	.captcha_handler(s_s_c_user_id=15,
                     s_s_c_session_id='8f460599bebe02cb0dd096b1fe70b089',
                     s_s_c_web_server_sign='edd2c221c05aece19f6db93a36b42272',
                     s_s_c_web_server_sign2='15989edaad1b4dc056ec8fa05abc7c9a',
                     page_url='https://www.keycaptcha.com/signup/')

'''
answer - это JSON строка с соответствующими полями

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

# капча решена верно, ошибка = 0
if answer['errorId'] == 0:
	# решение капчи
	print(answer['captchaSolve'])
	print(answer['taskId'])
# во время решения капчи возникли ошибки, ошибка = 1
elif answer['errorId'] == 1:
	# Тело ошибки, если есть
	print(answer['errorBody'])
