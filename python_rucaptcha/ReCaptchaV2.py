import requests
import time
from .config import url_request, url_response, app_key
from .errors import RuCaptchaError

class ReCaptchaV2:
	'''
	Класс служит для работы с новой ReCaptcha от Гугла и Invisible ReCaptcha.
	Для работы потребуется передать ключ от РуКапчи, затем ключ сайта(подробности его получения в описании на сайте)
	И так же ссылку на сайт.
	'''
	def __init__(self, rucaptcha_key, sleep_time=16):
		'''
		Инициализация нужных переменных.и
        :param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
		'''
		self.RUCAPTCHA_KEY = rucaptcha_key
		self.sleep_time = sleep_time
	
	# Работа с капчей
	# тестовый ключ сайта
	def captcha_handler(self, site_key, page_url):
		'''
		Метод отвечает за передачу данных на сервер для решения капчи
		:param site_key: Гугл-ключ сайта
		:param page_url: Ссылка на страницу на которой находится капча
		:return: В качестве ответа переждаётся строка которую нужно вставить для отправки гуглу на проверку
		'''
		captcha_sender = url_request+'?key={0}&method=userrecaptcha&googlekey={1}&pageurl={2}&json=1&soft_id={3}'\
							.format(self.RUCAPTCHA_KEY, site_key, page_url, app_key)
		
		# получаем ID капчи
		captcha_id = requests.request('GET', captcha_sender).json()
		# Фильтрация ошибки
		if captcha_id['status'] is 0:
			return RuCaptchaError(captcha_id['request'])

		captcha_id = captcha_id['request']
		
		# Ожидаем решения капчи 20 секунд
		time.sleep(self.sleep_time)
		
		while True:
			# отправляем запрос на результат решения капчи, если не решена ожидаем 6 секунд
			captcha_response = requests.request('GET', url_response+"?key={0}&action=get&id={1}&json=1"
			                                    .format(self.RUCAPTCHA_KEY, captcha_id))

			if captcha_response.json()['request'] == 'CAPCHA_NOT_READY':
				time.sleep(self.sleep_time)
			elif captcha_response.json()["status"] == 0:
				return RuCaptchaError(captcha_response.json()["request"])
			elif captcha_response.json()["status"] == 1:
				return captcha_response.json()['request']