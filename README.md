# python-rucaptcha
Python 3 library for RuCaptcha.

On [PyPi](https://pypi.python.org/pypi/python-rucaptcha/0.9).

## How to install?

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

Библиотека на языке Python 3 для работы с сервисом решения капчи [RuCaptcha](https://rucaptcha.com/).

На данный момент реализованы следующие методы:

1.[Решение капчи-изображения(большие и маленькие).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ImageCaptcha.py)

2.[Решение KeyCaptcha(пазл).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/KeyCaptcha.py) **НА ДАННЫЙ МОМЕНТ НЕ ПОДДЕРЖИВАЕТСЯ САМИМ СЕРВИСОМ RuCaptcha**

3.[Решение аудиокапчи. Используется для SolveMedia капчи.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/MediaCaptcha.py)

4.[Решение старой ReCaptcha v1.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ReCaptchaV1.py)

5.[Решение новой ReCaptcha v2.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ReCaptchaV2.py)

6.[Решение RotateCaptcha(повернуть изображение).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/RotateCaptcha.py)

7.[Решение текстовой капчи.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/TextCaptcha.py)

8.[Модуль для получения инофрмации о балансе аккаунта и отправке жалоб.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/RuCaptchaControl.py)
***
Кроме того, для тестирования различных типов капчи предоставляется [специальный сайт](http://85.255.8.26/), на котором собраны все имеющиеся типы капчи, с удобной системой тестирования ваших скриптов.

Присутствуют [примеры работы с библиотекой](https://github.com/AndreiDrang/python-rucaptcha/tree/master/CaptchaTester), которые демонстрируются на примере данного сайта

