import requests
import time
from config import url_request, url_response, app_key


class ReCaptchaV2:
	def __init__(self, rucaptcha_key, sleep_time=16):
		self.url_request = "http://2captcha.com/in.php"
		self.url_response = "http://2captcha.com/res.php"
		self.RUCAPTCHA_KEY = rucaptcha_key
		self.sleep_time = sleep_time
	
	# Работа с капчей
	# тестовый ключ сайта
	def captcha_handler(self, site_key, page_url):
		
		captcha_sender = url_request+'?key={0}&method=userrecaptcha&googlekey={1}&pageurl={2}&json=1&soft_id={3}'\
							.format(self.RUCAPTCHA_KEY, site_key, page_url, app_key)
		
		# получаем ID капчи
		answer = requests.request('GET', captcha_sender)
		captcha_id = answer.json()['request']
		
		# Ожидаем решения капчи 20 секунд
		time.sleep(self.sleep_time)
		
		while True:
			# отправляем запрос на результат решения капчи, если не решена ожидаем 6 секунд
			captcha_response = requests.request('GET', url_response+"?key={0}&action=get&id={1}&json=1"
			                                    .format(self.RUCAPTCHA_KEY, captcha_id))
			if captcha_response.json()["request"] == 'CAPCHA_NOT_READY':
				time.sleep(6)
			else:
				return captcha_response.json()["request"]
