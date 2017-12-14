# v.1.0.a
import requests
from python_rucaptcha import ImageCaptcha

"""
Этот пример показывает то как нужно работать с модулем для распознования обычной капчи изображением,
на примере нашего сайта.
В общем случае вам потребуется получение:
1. Получить ссылку на изображение капчи(сртрока 15 в примере)
2. Передать эту ссылку в модуль ImageCaptcha(строка 20 в примере)
"""
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = ''
# Для получения ссылки на обычную капчу нужно послать GET запрос с соответствующим парметром
image_link = requests.get("http://85.255.8.26/api/",
                          params={"captcha_type": "get_common_captcha"}).json()["captcha_src"]
"""
Тут нужно воспользоваться бибилотекой, отослать на решение ссылку на капчу и получить ответ
далее его записать в user_answer


Первый пример демонстрирует сохранеие файла изображения как обычного файла в папу
"""
user_answer_const = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY,
                                              save_format='const').captcha_handler(captcha_link=image_link)

"""
Второй пример демонстрирует сохранения файла как временного (temporary) - это стандартный вариант сохранения. 
Было выяснено, что он не работает с некоторыми видами капч - если возникают проблемы, то стоит использовать первый 
вариант
"""
user_answer_temp = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY,
                                             save_format='temp').captcha_handler(captcha_link=image_link)

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

if user_answer_const['errorId'] == 0:
    # решение капчи
    print(user_answer_const['captchaSolve'])
    print(user_answer_const['taskId'])
elif user_answer_const['errorId'] == 1:
    # Тело ошибки, если есть
    print(user_answer_const['errorBody'])

if user_answer_temp['errorId'] == 0:
    # решение капчи
    print(user_answer_temp['captchaSolve'])
    print(user_answer_temp['taskId'])
elif user_answer_temp['errorId'] == 1:
    # Тело ошибки, если есть
    print(user_answer_temp['errorBody'])

'''
Так же класс в качестве параметра может принимать список необязательных переменных, таких как:
phrase = 0, 
regsense = 0, 
numeric = 0, 
calc = 0, 
min_len = 0, 
max_len = 0, 
language = 0,
textinstructions = '', 
pingback = ''
и прочие.

Полный пример выглядит так:
'''
user_answer_full = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY,
                                             save_format='temp',
                                             phrase=0,
                                             regsense=0,
                                             numeric=0,
                                             calc=0,
                                             min_len=0,
                                             max_len=0,
                                             language=0,
                                             textinstructions='',
                                             pingback='').captcha_handler(captcha_link=image_link)

if user_answer_full['errorId'] == 0:
    # решение капчи
    print(user_answer_full['captchaSolve'])
    print(user_answer_full['taskId'])
elif user_answer_full['errorId'] == 1:
    # Тело ошибки, если есть
    print(user_answer_full['errorBody'])

"""
Асинхронный пример
Асинхронный способ поддерживает все параметры обычного метода
"""
import asyncio


async def run():
    try:
        answer_aio_image = await ImageCaptcha.aioImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY) \
            .captcha_handler(captcha_link=image_link)
        if answer_aio_image['errorId'] == 0:
            # решение капчи
            print(answer_aio_image['captchaSolve'])
            print(answer_aio_image['taskId'])
        elif answer_aio_image['errorId'] == 1:
            # Тело ошибки, если есть
            print(answer_aio_image['errorBody'])
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()



"""
Пример для работы с локальными файлами
"""
# папка в которой находится изображение, один из вариантов написания
captcha_file = r'D:\Python\933588.png'
# так же есть возможность передать так:
# captcha_file = 'D:\/Python\/933588.png'


# Асинхронный
import asyncio


async def run():
    try:
        answer_aio_local_image = await ImageCaptcha.aioImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY)\
								 .captcha_handler(captcha_file=captcha_file)
        if answer_aio_local_image['errorId'] == 0:
            # решение капчи
            print(answer_aio_local_image['captchaSolve'])
            print(answer_aio_local_image['taskId'])
        elif answer_aio_local_image['errorId'] == 1:
            # Тело ошибки, если есть
            print(answer_aio_local_image['errorBody'])
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

# Синхронный
user_answer_local = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_file=captcha_file)

if user_answer_local['errorId'] == 0:
    # решение капчи
    print(user_answer_local['captchaSolve'])
    print(user_answer_local['taskId'])
elif user_answer_local['errorId'] == 1:
    # Тело ошибки, если есть
    print(user_answer_local['errorBody'])
