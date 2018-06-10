# v.1.8
import asyncio

from python_rucaptcha import FunCaptcha

"""
Данный пример показывает работу модуля с FunCaptcha
"""

# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = 'aafb515dff0075f94b1f3328615bc0fd'

'''
Страница на которой находится FunCaptch: 
https://www.funcaptcha.com/demo
Данные взятые из этой страницы о данной капче:
'''
public_key = 'DE0B0BB7-1EE4-4D70-1853-31B835D4506B'
pageurl = 'https://www.funcaptcha.com/demo'


"""
Обычный пример для решения FunCaptcha
"""
answer = FunCaptcha.FunCaptcha(rucaptcha_key = RUCAPTCHA_KEY).captcha_handler(public_key=public_key, page_url=pageurl)

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

if answer['errorId'] == 0:
    # решение капчи
    print(answer['captchaSolve'])
    print(answer['taskId'])
elif answer['errorId'] == 1:
    # Тело ошибки, если есть
    print(answer['errorBody'])


"""
Пример асинхронного кода
"""


async def run():
    try:
        answer = await FunCaptcha.aioFunCaptcha(rucaptcha_key = '32275f9291ee237d74237cbe2ca2385f').captcha_handler(public_key=public_key, page_url=pageurl)
        if answer['errorId'] == 0:
            # решение капчи
            print(answer['captchaSolve'])
            print(answer['taskId'])
        elif answer['errorId'] == 1:
            # Тело ошибки, если есть
            print(answer['errorBody'])
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())
    loop.close()
