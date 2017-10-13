import requests
import time

from .config import url_request, url_response, app_key
from .errors import RuCaptchaError


class ReCaptchaV2:
	"""
	Класс служит для работы с новой ReCaptcha от Гугла и Invisible ReCaptcha.
	Для работы потребуется передать ключ от РуКапчи, затем ключ сайта(подробности его получения в описании на сайте)
	И так же ссылку на сайт.
	"""

	def __init__(self, rucaptcha_key, sleep_time = 16):
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
		payload = {'key': self.RUCAPTCHA_KEY,
				   'method': 'userrecaptcha',
				   'googlekey': site_key,
				   'pageurl': page_url,
				   'json': 1,
				   'soft_id': app_key,}
		# получаем ID капчи
		captcha_id = requests.post(url_request, data = payload)
		# Фильтрация ошибки
		if captcha_id.json()['status'] is 0:
			return RuCaptchaError(captcha_id.json()['request'])

		captcha_id = captcha_id.json()['request']

		# Ожидаем решения капчи 20 секунд
		time.sleep(self.sleep_time)

		while True:
			payload = {'key': self.RUCAPTCHA_KEY,
					   'action': 'get',
					   'id': captcha_id,
					   'json': 1,}
			# отправляем запрос на результат решения капчи, если не решена ожидаем
			captcha_response = requests.post(url_response, data = payload)

			if captcha_response.json()['request'] == 'CAPCHA_NOT_READY':
				time.sleep(self.sleep_time)
			elif captcha_response.json()["status"] == 0:
				return RuCaptchaError(captcha_response.json()["request"])
			elif captcha_response.json()["status"] == 1:
				return captcha_response.json()['request']
