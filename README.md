# python-rucaptcha

[![PyPI version](https://badge.fury.io/py/python-rucaptcha.svg)](https://badge.fury.io/py/python-rucaptcha)
[![Build Status](https://semaphoreci.com/api/v1/andreidrang/python-rucaptcha-2/branches/master/shields_badge.svg)](https://semaphoreci.com/andreidrang/python-rucaptcha-2)
[![Maintainability](https://api.codeclimate.com/v1/badges/aec93bb04a277cf0dde9/maintainability)](https://codeclimate.com/github/AndreiDrang/python-rucaptcha/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/698b08b078e94e03ab9ba8b098a2b41d)](https://app.codacy.com/app/drang.andray/python-rucaptcha?utm_source=github.com&utm_medium=referral&utm_content=AndreiDrang/python-rucaptcha&utm_campaign=Badge_Grade_Settings)
![Callback_Server_Status Run](https://img.shields.io/badge/Callback_Server_Status-Run-blue.svg)

Библиотека предназначена для разрабаотчиков ПО и служит для облегчения работы с API сервиса RuCaptcha.

Присутствуют [примеры работы с библиотекой](https://github.com/AndreiDrang/python-rucaptcha/tree/master/examples).

**Используется Python версии 3.6+.**

## How to install? Как установить?

### pip

```bash
pip install python-rucaptcha
```


### Source
```bash
git clone https://github.com/AndreiDrang/python-rucaptcha.git
cd python-rucaptcha
python setup.py install
```
***
По всем вопросам можете писать в [Telegram](https://t.me/joinchat/CD2EtQ5Pm0dmoSQQMTkVlw) чат.
***
### Последние обновления
**v.2.0** - Обновление JSON ответа, ключа с информацией об ошибке(создание собственного списка ошибок с уникальными `id`). 
Добавление в `errorBody` двух ключей: `text`(текст ошибки) и `id`(уникальный номер ошибки). [Таблица с ошибками и их номерами](#errors-table).
Замена `errorId` и его значений 1/0 на `error` и логические `True`(есть ошибка)/`False`(нет ошибки).

**v.2.2.1** - Вынесение методов для получению решений капчи (как синхронного так и асинхронного) в отдельный файл.

**v.2.3** - Удаление использования временных файлов(для хранения изображений) и замена их на переменную.

**v.2.4** - Добавление `callback`(pingback) параметра для работы со всеми видами капч. Добавление нового модуля для получения результатов решения капчи с сервера - [CallbackClient](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/CallbackClient.py). В примеры добавлен [асинхронный сервер(на aiohttp)](https://github.com/AndreiDrang/python-rucaptcha/blob/master/examples/callback_examples/callback_server.py) для обработки POST-запросов от RuCaptcha, а так же [`эмулятор RuCaptcha`](https://github.com/AndreiDrang/python-rucaptcha/blob/master/examples/callback_examples/rucaptcha_server.py), который высылает те же параметры что и настоящий сервер(подойдёт для тестирования обработки решений капчи). 

**v.2.5** - Добавление метода для решения `ReCaptcha v3`. Удаление модуля `MediaCaptcha` из библиотеки.

**v.2.5.3** - Добавление `contextmanager` ко всем методам решения капчи.

**v.2.5.4** - Добавление `GeeTest` метода. С синхронным и асинхронным исполнением.
***
### Будущие обновления
v.3.0 -  ...
***
### Реализованы следующие методы:

0.[Работа через callback(pingback)](https://github.com/AndreiDrang/python-rucaptcha/tree/master/examples/callback_examples).

Структура и принцип работы системы подробно [расписан в данной схеме](https://esk.one/p/i7oKYboABXJ/)

Краткий пример:

```python
import requests
from python_rucaptcha import ImageCaptcha, RuCaptchaControl, CallbackClient
# Введите ключ от сервиса RuCaptcha, из своего аккаунта
RUCAPTCHA_KEY = ""
# Ссылка на изображения для расшифровки
image_link = ""

# для начала работы нужно зарегистрировать IP/URL(делается с того же IP, который регистрируете):
RuCaptchaControl.RuCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY).additional_methods(action='add_pingback', addr='http://85.255.8.26/')
# проверка зарегистрированных адресов
answer = RuCaptchaControl.RuCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY).additional_methods(action='get_pingback', json=1)
print(answer)

# нужно придумать сложное название очереди(15+ знаков подойдёт) для получения результатов решения капчи
queue_name = 'ba86e77f9007_andrei_drang_7436e744_cute_queue'
# регистрируем очередь на callback сервере
answer = requests.post(f'http://85.255.8.26:8001/register_key', json={'key':queue_name, 'vhost': 'rucaptcha_vhost'})
print(answer.text)

# создаём задание в сервисе RuCaptcha и указываем `pingback` параметр
task_creation_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY, 
                                                     pingback=f'85.255.8.26:8001/rucaptcha/image_captcha/{queue_name}', 
                                                    ).captcha_handler(captcha_link=image_link)

print(task_creation_answer)
# Два варианта получения решения: кеш(результат хранится 1 час) и  rabbitmq очередь(результат удаляется после первого чтения)
# подключаемся к серверу и ждём решения капчи из кеша
callback_cache_response = CallbackClient.CallbackClient(task_id=task_creation_answer.get('id')).captcha_handler()
# подключаемся к серверу и ждём решения капчи из RabbitMQ queue
callback_queue_response = CallbackClient.CallbackClient(task_id=task_creation_answer.get('id'), queue_name=queue_name, call_type='queue').captcha_handler()

print(callback_cache_response)
print(callback_queue_response)
```

#### Если вы хотите запустить данный callback сервер у себя:

Небольшая [инструкция-памятка](https://github.com/AndreiDrang/python-rucaptcha/blob/master/examples/callback_examples/readme.txt) по шагам.

Установить и запустить веб-приложение, которое будет принимать POST-запросы, парсить их, и совершать прочую, нужную вам, магию.

[Пример такого сервера, написанный на aiohttp](https://github.com/AndreiDrang/python-rucaptcha/blob/master/examples/callback_examples/callback_server.py).

Все тесты можно проводить на локальном сервере, эмулируя POST-запросы от RuCaptcha при помощи [локального клиента](https://github.com/AndreiDrang/python-rucaptcha/blob/master/examples/callback_examples/rucaptcha_server.py).

Примеры создания реальных заданий для callback(pingback) способа вы можете посмотреть в [папке с примерами](https://github.com/AndreiDrang/python-rucaptcha/tree/master/examples), для конкретного метода капчи.

***

#### Работа обычным методом - ожидание решения капчи периодическим опросом сервера.

1.[Решение капчи-изображения(большие и маленькие).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ImageCaptcha.py)

Краткий пример:
```python
from python_rucaptcha import ImageCaptcha
# Введите ключ от сервиса RuCaptcha, из своего аккаунта
RUCAPTCHA_KEY = ""
# Ссылка на изображения для расшифровки
image_link = ""
# Возвращается JSON содержащий информацию для решения капчи
user_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_link=image_link)

if not user_answer['error']:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
elif user_answer['error']:
	# Тело ошибки, если есть
	print(user_answer['errorBody']['text'])
	print(user_answer['errorBody']['id'])
```

2.[Решение KeyCaptcha(пазл-капча).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/KeyCaptcha.py)

Краткий пример:
```python
from python_rucaptcha import KeyCaptcha
# Введите ключ от сервиса RuCaptcha, из своего аккаунта
RUCAPTCHA_KEY = ''

answer = KeyCaptcha.KeyCaptcha(rucaptcha_key=RUCAPTCHA_KEY) \
	.captcha_handler(s_s_c_user_id=15,
                     s_s_c_session_id='8f460599bebe02cb0dd096b1fe70b089',
                     s_s_c_web_server_sign='edd2c221c05aece19f6db93a36b42272',
                     s_s_c_web_server_sign2='15989edaad1b4dc056ec8fa05abc7c9a',
                     pageurl='https://www.keycaptcha.com/signup/')

# капча решена верно, ошибка = 0
if not answer['error']:
	# решение капчи
	print(answer['captchaSolve'])
	print(answer['taskId'])
# во время решения капчи возникли ошибки, ошибка = 1
elif answer['error']:
	# Тело ошибки, если есть
	print(answer['errorBody'])
``` 

3.[Решение ReCaptcha v2.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ReCaptchaV2.py)

Краткий пример:
```python
from python_rucaptcha import ReCaptchaV2
# Введите ключ от сервиса RuCaptcha, из своего аккаунта
RUCAPTCHA_KEY = ""
# G-ReCaptcha ключ сайта
SITE_KEY = ""
# Ссылка на страницу с капчёй
PAGE_URL = ""
# Возвращается JSON содержащий информацию для решения капчи
user_answer = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY,
                                                                                   page_url=PAGE_URL)

if not user_answer['error']:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
elif user_answer['error']:
	# Тело ошибки, если есть
	print(user_answer['errorBody']['text'])
	print(user_answer['errorBody']['id'])
```

4.[Решение новой ReCaptcha v3.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ReCaptchaV3.py)

Краткий пример:
```python
from python_rucaptcha import ReCaptchaV3
# Введите ключ от сервиса RuCaptcha, из своего аккаунта
RUCAPTCHA_KEY = ""
# G-ReCaptcha ключ сайта
SITE_KEY = ""
# Ссылка на страницу с капчёй
PAGE_URL = ""
# Значение параметра action, которые вы нашли в коде сайта
ACTION = 'verify'
# Требуемое значение рейтинга (score) работника, от 0.1(робот) до 0.9(человечный человек)
MIN_SCORE = 0.4
# Возвращается JSON содержащий информацию для решения капчи
user_answer = ReCaptchaV3.ReCaptchaV3(rucaptcha_key=RUCAPTCHA_KEY, 
				      action = ACTION, 
				      min_score = MIN_SCORE).captcha_handler(site_key=SITE_KEY,
					  				     page_url=PAGE_URL)

if not user_answer['error']:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
	print(user_answer['user_check'])
	print(user_answer['user_score'])
elif user_answer['error']:
	# Тело ошибки, если есть
	print(user_answer['errorBody']['text'])
	print(user_answer['errorBody']['id'])
```

5.[Решение RotateCaptcha(повернуть изображение).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/RotateCaptcha.py)

6.[Решение текстовой капчи.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/TextCaptcha.py)

Краткий пример:
```python
from python_rucaptcha import TextCaptcha
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = ''
# Вопрос
text_question = 'Если завтра суббота, то какой сегодня день?'

user_answer = TextCaptcha.TextCaptcha(rucaptcha_key = RUCAPTCHA_KEY).captcha_handler(captcha_text = text_question)

if not user_answer['error']:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
elif user_answer['error']:
	# Тело ошибки, если есть
	print(user_answer['errorBody']['text'])
	print(user_answer['errorBody']['id'])
```

7.[Решение FunCaptcha.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/FunCaptcha.py)

Краткий пример:
```python
from python_rucaptcha import FunCaptcha
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = ''

'''
Страница на которой находится FunCaptch: 
https://www.funcaptcha.com/demo
Данные взятые из этой страницы о данной капче:
'''
public_key = 'DE0B0BB7-1EE4-4D70-1853-31B835D4506B'
pageurl = 'https://www.funcaptcha.com/demo'

answer = FunCaptcha.FunCaptcha(rucaptcha_key = RUCAPTCHA_KEY).captcha_handler(public_key=public_key, page_url=pageurl)

if not answer['error']:
    # решение капчи
    print(answer['captchaSolve'])
    print(answer['taskId'])
elif answer['error']:
    # Тело ошибки, если есть
    print(answer['errorBody']['text'])
    print(answer['errorBody']['id'])
    
```
8.[Модуль для получения инофрмации о балансе аккаунта и отправке жалоб.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/RuCaptchaControl.py)
***
Кроме того, для тестирования различных типов капчи предоставляется [специальный сайт](http://85.255.8.26/), на котором собраны все имеющиеся типы капчи, с удобной системой тестирования ваших скриптов.
***
### Errors table
| Error ID       | Ошибка
| ------------- |:-------------:|
| -1      | Внутренняя ошибка (в соединении и т.п.), не относится к сервису RuCaptcha 

| Error ID       | in.php Rucaptcha код ошибки
| ------------- |:-------------:|
| 10      | ERROR_WRONG_USER_KEY 
| 11      | ERROR_KEY_DOES_NOT_EXIST 
| 12      | ERROR_ZERO_BALANCE      
| 13      | ERROR_PAGEURL 
| 14      | ERROR_NO_SLOT_AVAILABLE   
| 15      | ERROR_ZERO_CAPTCHA_FILESIZE         
| 16      | ERROR_TOO_BIG_CAPTCHA_FILESIZE 
| 17      | ERROR_WRONG_FILE_EXTENSION   
| 18      | ERROR_IMAGE_TYPE_NOT_SUPPORTED       
| 19      | ERROR_UPLOAD 
| 20      | ERROR_IP_NOT_ALLOWED  
| 21      | IP_BANNED        
| 22      | ERROR_BAD_TOKEN_OR_PAGEURL
| 23      | ERROR_GOOGLEKEY   
| 24      | ERROR_CAPTCHAIMAGE_BLOCKED     
| 25      | MAX_USER_TURN 

| Error ID      | res.php Rucaptcha код ошибки
| ------------- |:-------------:| 
| 30      | CAPCHA_NOT_READY 
| 31      | ERROR_CAPTCHA_UNSOLVABLE  
| 32      | ERROR_WRONG_ID_FORMAT       
| 33      | ERROR_WRONG_CAPTCHA_ID 
| 34      | ERROR_BAD_DUPLICATES   
| 35      | REPORT_NOT_RECORDED   

| Error ID      | NNNN Rucaptcha код ошибки
| ------------- |:-------------:|
| 40      | ERROR: 1001 
| 41      | ERROR: 1002  
| 42      | ERROR: 1003        
| 43      | ERROR: 1004 
| 44      | ERROR: 1005  
