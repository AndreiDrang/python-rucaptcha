import requests
import time
import urllib3
#site_key = "6Lf77CsUAAAAALLFD1wIhbfQRD07VxhvPbyQFaQJ"

class ReCaptcha:
	def __init__(self, recaptcha_api, sleep_time=5):
		self.url_request = "http://2captcha.com/in.php"
		self.url_response = "http://2captcha.com/res.php"
		self.RECAPTCHA_KEY = recaptcha_api
		self.sleep_time = sleep_time

	#Работа с капчей
	#тестовый ключ сайта
	def captcha_handler(self, site_key="6Lf77CsUAAAAALLFD1wIhbfQRD07VxhvPbyQFaQJ", page_url='http://127.0.0.1:5000/'):
		captcha_download = 'http://rucaptcha.com/in.php?key={0}&method=userrecaptcha&googlekey={1}&pageurl={2}'\
			.format(self.RECAPTCHA_KEY, site_key, page_url)
		
		# проверяем капчу
		http = urllib3.PoolManager()
		answer = http.request('GET', captcha_download)
		
		#получаем ID капчи
		print(str(answer.data), '!!!')
		captcha_id = (str(answer.data).split('|'))
		answer = 'http://rucaptcha.com/res.php?key={0}&action=get&id={1}'.format(self.RECAPTCHA_KEY, captcha_id)
		
		# Ожидаем решения капчи
		time.sleep(self.sleep_time)
		while True:
			captcha_response = requests.request('GET', answer)
			if str(captcha_response.content) == 'CAPCHA_NOT_READY':
				time.sleep(self.sleep_time)
			else:
				print(str(captcha_response.content).split('|'), '!!!!')
				return str(captcha_response.content).split('|')[1]



