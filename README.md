# python-rucaptcha

[![PyPI version](https://badge.fury.io/py/python-rucaptcha.svg)](https://badge.fury.io/py/python-rucaptcha)
[![Maintainability](https://api.codeclimate.com/v1/badges/aec93bb04a277cf0dde9/maintainability)](https://codeclimate.com/github/AndreiDrang/python-rucaptcha/maintainability)


Библиотека предназначена для разработчиков ПО и служит для облегчения работы с API сервиса RuCaptcha.

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
По всем вопросам можете писать в [Telegram](https://t.me/pythoncaptcha) чат.
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

**v.2.6.3** - Добавление `Distil` метода. С синхронным и асинхронным исполнением.

**v.2.6.4** - Добавление `HCaptcha` метода. С синхронным и асинхронным исполнением.

**v.2.6.5** - Добавление `CapyPuzzle` метода. С синхронным и асинхронным исполнением.

**v.3.0** - Удаление кастомных ошибок и вывода текста о них.
1. Замена структуры: 
    ```json
    {
      "errorBody":
        {
          "text": "some text",
          "id": 1
        }
    }
    ```
1. На структуру: 
    ```json
    {
      "errorBody": "ERROR_NAME or error text description"
    }
    ```
***
### Будущие обновления
v.4.0 - Переработка классов и методов. Добавление наследований и сериализаторов. Собственный Callback-сервер - deprecated.
***
### Реализованы следующие методы:

#### Работа обычным методом - ожидание решения капчи периодическим опросом сервера.

1. [Решение капчи-изображения.](./python_rucaptcha/ImageCaptcha.py)

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
	print(user_answer ['errorBody'])
```

2. [Решение KeyCaptcha(пазл-капча).](./python_rucaptcha/KeyCaptcha.py)

```python
from python_rucaptcha import KeyCaptcha
# Введите ключ от сервиса RuCaptcha, из своего аккаунта
RUCAPTCHA_KEY = ''

answer = KeyCaptcha.KeyCaptcha(rucaptcha_key=RUCAPTCHA_KEY) \
	.captcha_handler(key_params = {
				's_s_c_user_id':15,
                		's_s_c_session_id':'8f460599bebe02cb0dd096b1fe70b089',
                		's_s_c_web_server_sign':'edd2c221c05aece19f6db93a36b42272',
                		's_s_c_web_server_sign2':'15989edaad1b4dc056ec8fa05abc7c9a',
                		'pageurl':'https://www.keycaptcha.com/signup/'
			}
	)

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

3. [Решение ReCaptcha v2.](./python_rucaptcha/ReCaptchaV2.py)

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
	print(user_answer ['errorBody'])
```

4. [Решение ReCaptcha v3.](./python_rucaptcha/ReCaptchaV3.py)

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
user_answer = ReCaptchaV3.ReCaptchaV3(
                                    rucaptcha_key=RUCAPTCHA_KEY, 
				                    action = ACTION, 
				                    min_score = MIN_SCORE).captcha_handler(
                                                site_key=SITE_KEY,
					  				            page_url=PAGE_URL
                                            )

if not user_answer['error']:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
	print(user_answer['user_check'])
	print(user_answer['user_score'])
elif user_answer['error']:
	# Тело ошибки, если есть
	print(user_answer ['errorBody'])
```

5. [Решение RotateCaptcha(повернуть изображение).](./python_rucaptcha/RotateCaptcha.py)

6. [Решение текстовой капчи.](./python_rucaptcha/TextCaptcha.py)

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
	print(user_answer ['errorBody'])
```

7. [Решение FunCaptcha.](./python_rucaptcha/FunCaptcha.py)

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
    print(answer ['errorBody'])
    
```
8. [Модуль для получения инофрмации о балансе аккаунта и отправке жалоб.](./python_rucaptcha/RuCaptchaControl.py)

```python
from python_rucaptcha.RuCaptchaControl import RuCaptchaControl
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = ''

JsSha1 = "af2d0557c23ff2d8f40ccf4bec57e480704634e9"
JsUri = "http://www.targetwebsite.com/pvvhnzyazwpzgkhv.js"
JsData = "IWZ1bmN0fewfwefwefwef9905j0g4905jh9046hj3cpCg=="

answer = RuCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY).additional_methods(
            action="getbalance"
        )

if not answer["error"]:
    print("Your balance is: ", answer["serverAnswer"], " rub.")

elif answer["error"]:
    # Тело ошибки, если есть
    print(answer["errorBody"])

# Пример отправки жалобы на неправильно решённую капчу под ID "666"
wrong_captcha_id = 666

answer = RuCaptchaControl(rucaptcha_key=RUCAPTCHA_KEY).additional_methods(
            action="reportbad", id=wrong_captcha_id
        )

# Если заявка принята
if not answer["error"]:
    print("Заявка принята.")

# Если возникла ошибка
elif answer["error"]:
    print(answer["errorBody"])
```
9. [Решение HCaptcha.](./python_rucaptcha/HCaptcha.py)

```python
from python_rucaptcha.HCaptcha import HCaptcha
RUCAPTCHA_KEY = ''

website_link = "https://secure2.e-konsulat.gov.pl/Uslugi/RejestracjaTerminu.aspx?IDUSLUGI=1&IDPlacowki=94"
data_sitekey = "39fccce0-e3e3-4f9d-a942-ea415c102beb"

answer = HCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(
    site_key=data_sitekey, page_url=website_link
)

if not answer['error']:
    # решение капчи
    print(answer['captchaSolve'])
    print(answer['taskId'])
elif answer['error']:
    # Тело ошибки, если есть
    print(answer ['errorBody'])
    
```
10. [Решение CapyPuzzle.](./python_rucaptcha/CapyPuzzle.py)

```python
from python_rucaptcha.CapyPuzzle import CapyPuzzle
RUCAPTCHA_KEY = ''

captchakey="PUZZLE_Cme4hZLjuZRMYC3uh14C52D3uNms5w"
page_url="https://www.capy.me/account/register/"

answer = CapyPuzzle(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(
            captchakey=captchakey, page_url=page_url
        )

if not answer['error']:
    # решение капчи
    print(answer['captchaSolve'])
    print(answer['taskId'])
elif answer['error']:
    # Тело ошибки, если есть
    print(answer ['errorBody'])
    
```
***
Кроме того, для тестирования различных типов капчи предоставляется [специальный сайт](https://pythoncaptcha.xyz/), на котором собраны все имеющиеся типы капчи, с удобной системой тестирования ваших скриптов.
***
### Errors description. Описания ошибок
**В обоих ссылках находятся валидные описания ошибок**
1. https://rucaptcha.com/api-rucaptcha#in_errors
1. https://rucaptcha.docs.apiary.io/#reference/2

![img.png](files/img.png)