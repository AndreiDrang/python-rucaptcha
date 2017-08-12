import requests
import ClickCaptcha

#pass your api key
RUCAPTCHA_KEY = ''
#pass link to recaptcha image as parameter
clickcaptcha_link = 'http://85.255.8.26/{0}'.format("")
#create an object and let it do the wordk
click_captcha = ClickCaptcha(RUCAPTCHA_KEY)
coordinates = click_captcha.captcha_handler(clickcaptcha_link)
print(coordinates)