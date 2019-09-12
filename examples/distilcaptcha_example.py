import asyncio

from python_rucaptcha.DistilCaptcha import DistilCaptcha, aioDistilCaptcha

"""
Документация на РуКапче - https://rucaptcha.com/distil-api-ru
"""

# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = "aafb515dff0075f94b1f3328615bc0bd"
"""
JsSha1 - контрольная сумма SHA1 для javascript библиотеки
JsUri - URL javascript библиотеки
JsData - данные библиотеки, закодированные в base64
"""
JsSha1 = "af2d0557c23ff2d8f40ccf4bec57e480704634e9"
JsUri = "http://www.targetwebsite.com/pvvhnzyazwpzgkhv.js"
JsData = "IWZ1bmN0fewfwefwefwef9905j0g4905jh9046hj3cpCg=="

"""
contextmanager пример
"""

result = DistilCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(
    JsSha1=JsSha1, JsUri=JsUri, JsData=JsData
)
print(result)

# синхронный пример contextmanager
with DistilCaptcha(rucaptcha_key=RUCAPTCHA_KEY) as dist_captcha:
    result = dist_captcha.captcha_handler(JsSha1=JsSha1, JsUri=JsUri, JsData=JsData)
    print(result)

# асинхронный пример contextmanager
async def aiocontext():
    with aioDistilCaptcha(rucaptcha_key=RUCAPTCHA_KEY) as ob:
        result = await ob.captcha_handler(JsSha1=JsSha1, JsUri=JsUri, JsData=JsData)
        print(result)


loop = asyncio.get_event_loop()
loop.run_until_complete(aiocontext())
loop.close()
