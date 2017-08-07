import requests
import time
import urllib3
#site_key = "6Lf77CsUAAAAALLFD1wIhbfQRD07VxhvPbyQFaQJ"

class ReCaptcha:
	def __init__(self, recaptcha_api, sleep_time=5):
		self.RECAPTCHA_KEY = recaptcha_api
		self.sleep_time = sleep_time

	#Работа с капчей
	#тестовый ключ сайта
	def captcha_handler(self, site_key):
		captcha_download = 'http://rucaptcha.com/in.php?key={0}&method=userrecaptcha&googlekey={1}'\
			.format(self.RECAPTCHA_KEY, site_key)
		# проверяем капчу
		http = urllib3.PoolManager()
		answer = http.request('GET', captcha_download)
		print(answer)
		#получаем ID капчи
		captcha_id = (str(answer.data).split('|'))
		answer = 'http://rucaptcha.com/res.php?key={0}&action=get&id={1}'.format(self.RECAPTCHA_KEY, captcha_id)
		# Ожидаем решения капчи
		time.sleep(self.sleep_time)
		while True:
			captcha_response = requests.request('GET', answer)
			if str(captcha_response.content) == 'CAPCHA_NOT_READY':
				time.sleep(self.sleep_time)
			else:
				return str(captcha_response.content).split('|')[1]



