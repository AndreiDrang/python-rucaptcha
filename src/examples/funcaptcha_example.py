from python_rucaptcha.enums import FunCaptchaEnm
from python_rucaptcha.FunCaptcha import FunCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad91111111111111768608fa758570"


publickey = "69A21A01-CC7B-B9C6-1111-E7FA06677FFC"
pageurl = "https://api.funcaptcha.com/fc/api/nojs/"
surl = "https://client-api.arkoselabs.com"


with FunCaptcha(
    rucaptcha_key=RUCAPTCHA_KEY, pageurl=pageurl, publickey=publickey, surl=surl, method=FunCaptchaEnm.FUNCAPTCHA.value
) as fun_captcha:
    result = fun_captcha.captcha_handler()
    print(result)
