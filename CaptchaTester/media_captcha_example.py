import requests

from python_rucaptcha import MediaCaptcha, CallbackClient, RuCaptchaControl

"""
!!!ВАЖНО!!!
Обязательно, перед работой с данным модулем, - создайте папку "mediacaptcha_audio"
!!!ВАЖНО!!!

UPDATE 2.4
Добавление возможности применять callback при получении ответа капчи
Для этого в класс нужно передать параметр `pingback` со значением URL'a для ожидания ответа, к примеру - 85.255.8.26/media_captcha
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


"""
Callback пример
"""
# нужно передать IP/URL ранее зарегистрированного сервера
server_ip = '85.255.8.26'
# и по желанию - порт на сервере который слушает ваше веб-приложение
server_port = 8001
# регистрация нового домена для callback/pingback
answer = RuCaptchaControl.RuCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY).additional_methods(action='add_pingback', addr=f'http://{server_ip}:{server_port}/', json=1)
print(answer)

# нужно придумать ЛЮБОЕ сложное название очереди(15+ знаков подойдёт)
queue_name = 'ba86e77f9007_andrei_drang_7436e7444060657442674_cute_media_queue'
# регистрируем очередь на callback сервере
answer = requests.post(f'http://{server_ip}:{server_port}/register_key', json={'key':queue_name})

# если очередь зарегистрирована
if answer.text == 'OK':
    # IP адрес должен быть ЗАРАНЕЕ зарегистрирован в системе (подробонсти смотри в `CaptchaTester/rucaptcha_control_example.py`)
    # создаём задание на сервере, ответ на которое придёт на заданный pingback URL в виде POST запроса
    task_creation_answer = MediaCaptcha.MediaCaptcha(rucaptcha_key=RUCAPTCHA_KEY, 
                                                     solveaudio=True,
                                                     pingback=f'85.255.8.26:8001/rucaptcha/media_captcha/{queue_name}', 
                                                    ).captcha_handler(audio_name=solve_media_file)

    print(task_creation_answer)

    # подключаемся к серверу и ждём решения капчи из кеша
    callback_server_response = CallbackClient.CallbackClient(task_id=task_creation_answer.get('id')).captcha_handler()

    print(callback_server_response)

    # подключаемся к серверу и ждём решения капчи из RabbitMQ queue
    callback_server_response = CallbackClient.CallbackClient(task_id=task_creation_answer.get('id'), queue_name=queue_name, call_type='queue').captcha_handler()

    print(callback_server_response)
