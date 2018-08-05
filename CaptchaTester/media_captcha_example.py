from python_rucaptcha import MediaCaptcha

"""
!!!ВАЖНО!!!
Обязательно, перед работой с данным модулем, - создайте папку "mediacaptcha_audio"
!!!ВАЖНО!!!

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

"""
Этот пример показывает то как нужно работать с модулем для распознования аудио капчи,
на примере нашего сайта и скачаных зарание аудиофайлов.
В общем случае вам потребуется получение:
1. Скачать аудиофайл в зарание созданную папку "mediacaptcha_audio", либо же передать ссылку для скачивания на файл
2. Передать этот параметр в метод MediaCaptcha и так же указать тип капчи из которой получен аудиофайл recaptchavoice, solveaudio.
"""
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = ''
# Примеры ссылок для различных типов капчи
solve_media_link = "http://85.255.8.26/static/media/solvemedia_audio/solvemedia_runphrough.mp3"
recaptcha_media_link = "http://85.255.8.26/static/media/solvemedia_audio/recaptcha_55914.mp3"
# Примеры файлов для различных типов капчи
solve_media_file = "solvemedia_pzalcbniuf.mp3"
recaptcha_media_file = "recaptcha_55914.mp3"

"""
Тут нужно воспользоваться бибилотекой.
Данный пример показывает работу библиотеки с ссылками, для двух разных выдов капчи
"""
solve_audio_user_answer = MediaCaptcha.MediaCaptcha(RUCAPTCHA_KEY, solveaudio=True).captcha_handler(audio_download_link=solve_media_link)
recaptcha_audio_user_answer = MediaCaptcha.MediaCaptcha(RUCAPTCHA_KEY, recaptchavoice=True).captcha_handler(audio_download_link=recaptcha_media_link)
if not solve_audio_user_answer['error']:
    # решение капчи
    print(solve_audio_user_answer['captchaSolve'])
    print(solve_audio_user_answer['taskId'])
elif solve_audio_user_answer['error']:
    # Тело ошибки, если есть
    print(solve_audio_user_answer['errorBody']['text'])
    print(solve_audio_user_answer['errorBody']['id'])

if not recaptcha_audio_user_answer['error']:
    # решение капчи
    print(recaptcha_audio_user_answer['captchaSolve'])
    print(recaptcha_audio_user_answer['taskId'])
elif recaptcha_audio_user_answer['error']:
    # Тело ошибки, если есть
    print(recaptcha_audio_user_answer['errorBody']['text'])
    print(recaptcha_audio_user_answer['errorBody']['id'])
'''
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

"""
Тут нужно воспользоваться бибилотекой.
Данный пример показывает работу библиотеки с файлами, для двух разных выдов капчи
"""
solve_audio_file_answer = MediaCaptcha.MediaCaptcha(RUCAPTCHA_KEY, solveaudio=True).captcha_handler(audio_name=solve_media_file)
recaptcha_audio_file_answer = MediaCaptcha.MediaCaptcha(RUCAPTCHA_KEY, recaptchavoice=True).captcha_handler(audio_name=recaptcha_media_file)

if not solve_audio_file_answer['error']:
    # решение капчи
    print(solve_audio_file_answer['captchaSolve'])
    print(solve_audio_file_answer['taskId'])
elif solve_audio_file_answer['error']:
    # Тело ошибки, если есть
    print(solve_audio_file_answer['errorBody']['text'])
    print(solve_audio_file_answer['errorBody']['id'])

if not recaptcha_audio_file_answer['error']:
    # решение капчи
    print(recaptcha_audio_file_answer['captchaSolve'])
    print(recaptcha_audio_file_answer['taskId'])
elif recaptcha_audio_file_answer['error']:
    # Тело ошибки, если есть
    print(recaptcha_audio_file_answer['errorBody']['text'])
    print(recaptcha_audio_file_answer['errorBody']['id'])
