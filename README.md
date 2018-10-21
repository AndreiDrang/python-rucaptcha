# python-rucaptcha

[![PyPI version](https://badge.fury.io/py/python-rucaptcha.svg)](https://badge.fury.io/py/python-rucaptcha)
[![Maintainability](https://api.codeclimate.com/v1/badges/aec93bb04a277cf0dde9/maintainability)](https://codeclimate.com/github/AndreiDrang/python-rucaptcha/maintainability)


Библиотека предназначена для разрабаотчиков ПО и служит для облегчения работы с API сервиса RuCaptcha.

Присутствуют [примеры работы с библиотекой](https://github.com/AndreiDrang/python-rucaptcha/tree/master/CaptchaTester).

Если вы работаете на OS Windows с ImageCaptcha - используйте *ImageCaptcha.ImageCaptcha(save_format='const')*.

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
**v.1.6.2** - Добавлена поддержка прокси для Капчи-Изображения(асинхронный и синхронные методы). Добавлена KeyCaptcha и примеры для неё.

**v.1.6.3** - Добавлена возможности выбора между двумя сервисами: `2captcha`(стандартный метод) и `rucaptcha`, для этого в каждый класс капчи 
добавлен новый параметр - `service_type`. Соответственно он принимает один из двух параметров-названий сервиса:
 
 _ImageCaptcha.ImageCaptcha(... ,_ **service_type = '2captcha'**_).captcha_handler(...)_ или _ImageCaptcha.ImageCaptcha(... ,_ **service_type = 'rucaptcha'**_).captcha_handler(...)_

Аналогично для всех остальных видов капчи.

**v.1.6.4** - Добавлена поддержка прокси для ReCaptchaV2 & Invisible ReCaptcha.

**v.1.6.6** - Много правок в обработке ошибок от сервера(правка `ERROR: NNNN`) и системных(при чтении капчи-изображения).
Добавление `max_retries=5` попыток подключения к серверу(для синхронного метода) всех типов капчи. 
Добавление обязательного параметра для решения `Invisible ReCaptcha` - `invisible`.
Добавление `base64` в качестве варианта передачи изображения в base64 формате в `captcha_handler`.
Удаление нерабочего вида капчи - `ReCaptcha v1`. Переезд синтаксиса форматирования строк на `Python 3.6` - `f''`.
Обновление примеров, `__doc__` для методов классов(с учётом новых параметров.) 

**v.1.8** - Добавление FunCaptcha. Добавление асинхронного метода для KeyCaptcha. Удаление `raise` из кода и замена этого на корректное возвращение ошибки через JSON. 

**v.2.0** - Обновление JSON ответа, ключа с информацией об ошибке(создание собственного списка ошибок с уникальными `id`). 
Добавление в `errorBody` двух ключей: `text`(текст ошибки) и `id`(уникальный номер ошибки). [Таблица с ошибками и их номерами](#errors-table).
Замена `errorId` и его значений 1/0 на `error` и логические `True`(есть ошибка)/`False`(нет ошибки).

**v.2.2.1** - Вынесение методов для получению решений капчи (как синхронного так и асинхронного) в отдельный файл.
***
### Будущие обновления
v.3.0 -  ...
***
### На данный момент реализованы следующие методы:

1.[Решение капчи-изображения(большие и маленькие).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ImageCaptcha.py)

Краткий пример:
```python
from python_rucaptcha import ImageCaptcha
# Введите ключ от сервиса RuCaptcha, из своего аккаунта
RUCAPTCHA_KEY = ""
# Ссылка на изображения для расшифровки
image_link = ""
# Возвращается строка-расшифровка капчи
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
                     page_url='https://www.keycaptcha.com/signup/')

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

3.[Решение аудиокапчи. Используется для SolveMedia капчи.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/MediaCaptcha.py) ***НЕ ПОДДЕРЖИВАЕТСЯ СЕРВИСОМ RuCaptcha***

4.[Решение новой ReCaptcha v2.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ReCaptchaV2.py)

Краткий пример:
```python
from python_rucaptcha import ReCaptchaV2
# Введите ключ от сервиса RuCaptcha, из своего аккаунта
RUCAPTCHA_KEY = ""
# G-ReCaptcha ключ сайта
SITE_KEY = ""
# Ссылка на страницу с капчёй
PAGE_URL = ""
# Возвращается строка-расшифровка капчи
user_answer = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY, page_url=PAGE_URL)

if not user_answer['error']:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
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

7.[Решение FunCaptcha.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/TextCaptcha.py)
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