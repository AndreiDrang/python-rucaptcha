# python-rucaptcha

[![PyPI version](https://badge.fury.io/py/python-rucaptcha.svg)](https://badge.fury.io/py/python-rucaptcha)

Библиотека предназначена для разрабаотчиков ПО и служит для облегчения работы с API сервиса RuCaptcha.

**Добавлен асинхронный способ работы, все примеры показаны в [папке с примерами](https://github.com/AndreiDrang/python-rucaptcha/tree/master/CaptchaTester)**.

Если вы работаете на OS Windows с ImageCaptcha - используйте *captcha_handler(save_format = 'const')*.

Если нужна версия без асинхронности вообще - качайте [релиз 1.0](https://github.com/AndreiDrang/python-rucaptcha/releases)

**Используется Python версии 3.5.3+.**

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
v.1.6.2 - Добавлена поддержка прокси для Капчи-Изображения(асинхронный и синхронные методы). Добавлена KeyCaptcha и примеры для неё.
***
### Будущие обновления
v.1.6.* - Добавление асинхронного метода для KeyCaptcha.

v.1.7.* - Добавление FunCaptcha.
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

if user_answer['errorId'] == 0:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
elif user_answer['errorId'] == 1:
	# Тело ошибки, если есть
	print(user_answer['errorBody'])
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
if answer['errorId'] == 0:
	# решение капчи
	print(answer['captchaSolve'])
	print(answer['taskId'])
# во время решения капчи возникли ошибки, ошибка = 1
elif answer['errorId'] == 1:
	# Тело ошибки, если есть
	print(answer['errorBody'])
``` 

3.[Решение аудиокапчи. Используется для SolveMedia капчи.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/MediaCaptcha.py) ***НЕ ПОДДЕРЖИВАЕТСЯ СЕРВИСОМ RuCaptcha***

4.[Решение старой ReCaptcha v1.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ReCaptchaV1.py)

5.[Решение новой ReCaptcha v2.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ReCaptchaV2.py)

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

if user_answer['errorId'] == 0:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
elif user_answer['errorId'] == 1:
	# Тело ошибки, если есть
	print(user_answer['errorBody'])
```

6.[Решение RotateCaptcha(повернуть изображение).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/RotateCaptcha.py)

7.[Решение текстовой капчи.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/TextCaptcha.py)
Краткий пример:
```python
from python_rucaptcha import TextCaptcha
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = ''
# Вопрос
text_question = 'Если завтра суббота, то какой сегодня день?'

user_answer = TextCaptcha.TextCaptcha(rucaptcha_key = RUCAPTCHA_KEY).captcha_handler(captcha_text = text_question)

if user_answer['errorId'] == 0:
	# решение капчи
	print(user_answer['captchaSolve'])
	print(user_answer['taskId'])
elif user_answer['errorId'] == 1:
	# Тело ошибки, если есть
	print(user_answer['errorBody'])
```
8.[Модуль для получения инофрмации о балансе аккаунта и отправке жалоб.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/RuCaptchaControl.py)
***
Кроме того, для тестирования различных типов капчи предоставляется [специальный сайт](http://85.255.8.26/), на котором собраны все имеющиеся типы капчи, с удобной системой тестирования ваших скриптов.

Присутствуют [примеры работы с библиотекой](https://github.com/AndreiDrang/python-rucaptcha/tree/master/CaptchaTester), которые демонстрируются на примере данного сайта
