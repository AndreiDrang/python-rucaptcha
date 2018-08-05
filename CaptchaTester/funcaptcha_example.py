# v.1.8
import asyncio

from python_rucaptcha import FunCaptcha

"""
Данный пример показывает работу модуля с FunCaptcha
"""

"""
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
taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
error - False - если всё хорошо, True - если есть ошибка,
errorBody - полная информация об ошибке: 
    {
        text - Развернётое пояснение ошибки
        id - уникальный номер ошибка в ЭТОЙ бибилотеке
    }
'''

if not answer['error']:
    # решение капчи
    print(answer['captchaSolve'])
    print(answer['taskId'])
elif answer['error']:
    # Тело ошибки, если есть
    print(answer['errorBody']['text'])
    print(answer['errorBody']['id'])


"""
Пример асинхронного кода
"""


async def run():
    try:
        answer = await FunCaptcha.aioFunCaptcha(rucaptcha_key = '32275f9291ee237d74237cbe2ca2385f').captcha_handler(public_key=public_key, page_url=pageurl)
        if not answer['error']:
            # решение капчи
            print(answer['captchaSolve'])
            print(answer['taskId'])
        elif answer['error']:
            # Тело ошибки, если есть
            print(answer['errorBody']['text'])
            print(answer['errorBody']['id'])
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())
    loop.close()
