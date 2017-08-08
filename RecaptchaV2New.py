import requests
import time
import urllib3


# site_key = "6Lf77CsUAAAAALLFD1wIhbfQRD07VxhvPbyQFaQJ"

class ReCaptcha:
	def __init__(self, recaptcha_api, sleep_time=5):
		self.url_request = "http://2captcha.com/in.php"
		self.url_response = "http://2captcha.com/res.php"
		self.RECAPTCHA_KEY = recaptcha_api
		self.sleep_time = sleep_time
	
	# Работа с капчей
	# тестовый ключ сайта
	def captcha_handler(self, site_key="6Lf77CsUAAAAALLFD1wIhbfQRD07VxhvPbyQFaQJ", page_url='http://127.0.0.1:5000/'):
		
		captcha_download = 'http://rucaptcha.com/in.php?key={0}&method=userrecaptcha&googlekey={1}&pageurl={2}&json=1' \
			.format(self.RECAPTCHA_KEY, site_key, page_url)
		
		# получаем ID капчи
		answer = requests.request('GET', captcha_download)
		captcha_id = answer.json()['request']
		
		# Ожидаем решения капчи 20 секунд
		time.sleep(self.sleep_time * 4)
		
		while True:
			# отправляем запрос на результат решения капчи, если не решена ожидаем 6 секунд
			captcha_response = requests.request('GET', "http://rucaptcha.com/res.php?key={0}&action=get&id={1}&json=1"
			                                    .format(self.RECAPTCHA_KEY, captcha_id))
			if captcha_response.json()["request"] == 'CAPCHA_NOT_READY':
				time.sleep(6)
			else:
				return captcha_response.json()["request"]