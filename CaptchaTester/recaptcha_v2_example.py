from python_rucaptcha import ReCaptchaV2



RUCAPTCHA_KEY = ""
"""
Этот пример показывает работу модуля решения ReCaptcha v2 New
"""
# Введите ключ от рукапчи из своего аккаунта
SITE_KEY = '6Lf77CsUAAAAALLFD1wIhbfQRD07VxhvPbyQFaQJ'
PAGE_URL = 'http://85.255.8.26/'

# Пример работы с модулем ReCaptchaV2
answer = ReCaptchaV2.ReCaptchaV2(recaptcha_api=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY, page_url=PAGE_URL)
"""
answer - это и есть ключ решения рекапчи
"""
print(answer)


"""
Этот пример показывает работу модуля решения Invisible ReCaptcha
"""

SITE_KEY = '6LcC7SsUAAAAAN3AOB-clPIsrKfnBUlO2QkC_vQ7'
PAGE_URL = 'http://85.255.8.26/invisible_recaptcha/'

# Пример работы с модулем ReCaptchaV2
answer = ReCaptchaV2.ReCaptchaV2(recaptcha_api=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY, page_url=PAGE_URL)
"""
answer - это и есть ключ решения рекапчи
"""
print(answer)