import requests
import time


class TextCaptcha:
	def __init__(self, recaptcha_api, sleep_time=6):
		self.url_request = "http://2captcha.com/in.php"
		self.url_response = "http://2captcha.com/res.php"
		self.RECAPTCHA_KEY = recaptcha_api
		self.sleep_time = sleep_time

	def handle_captcha(self, captcha_text):
		# Создаём пайлоад, вводим ключ от сайта, выбираем метод ПОСТ и ждём ответа. в JSON-формате
		payload = {"key": self.RECAPTCHA_KEY,
					"method": "textcaptcha",
					"json": 1,
					"textinstructions": captcha_text}
		# Отправляем на рукапча текст капчи и ждём ответа
		#  в результате получаем JSON ответ с номером решаемой капчи
		captcha_id = (requests.request('POST',
										"http://rucaptcha.com/in.php",
										data=payload).json())['request']
		# Ожидаем решения капчи
		time.sleep(self.sleep_time)
		while True:
			# отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
			#  если всё ок - идём дальше
			captcha_response = requests.request('GET',
												"http://rucaptcha.com/res.php?key={0}&action=get&id={1}&json=1"
												.format(self.RECAPTCHA_KEY, captcha_id))
			if captcha_response.json()["request"] == 'CAPCHA_NOT_READY':
				time.sleep(self.sleep_time)
			else:
				return captcha_response.json()['request']
