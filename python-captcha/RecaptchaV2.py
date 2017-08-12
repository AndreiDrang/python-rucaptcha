import requests
import time


class ReCaptchaV2:
	def __init__(self, recaptcha_api, sleep_time=16):
		self.url_request = "http://2captcha.com/in.php"
		self.url_response = "http://2captcha.com/res.php"
		self.RECAPTCHA_KEY = recaptcha_api
		self.sleep_time = sleep_time
	
	# Работа с капчей
	# тестовый ключ сайта
	def captcha_handler(self, site_key, page_url):
		
		captcha_sender = 'http://rucaptcha.com/in.php?key={0}&method=userrecaptcha&googlekey={1}&pageurl={2}&json=1'\
							.format(self.RECAPTCHA_KEY, site_key, page_url)
		
		# получаем ID капчи
		answer = requests.request('GET', captcha_sender)
		captcha_id = answer.json()['request']
		
		# Ожидаем решения капчи 20 секунд
		time.sleep(self.sleep_time)
		
		while True:
			# отправляем запрос на результат решения капчи, если не решена ожидаем 6 секунд
			captcha_response = requests.request('GET', "http://rucaptcha.com/res.php?key={0}&action=get&id={1}&json=1"
			                                    .format(self.RECAPTCHA_KEY, captcha_id))
			if captcha_response.json()["request"] == 'CAPCHA_NOT_READY':
				time.sleep(6)
			else:
				return captcha_response.json()["request"]
			
#print(ReCaptchaV2(recaptcha_api="").captcha_handler(site_key="6LcC7SsUAAAAAN3AOB-clPIsrKfnBUlO2QkC_vQ7", page_url='http://85.255.8.26/invisible_recaptcha/'))