import requests
import time

from .config import url_request, url_response, app_key
from .errors import RuCaptchaError


class TextCaptcha:
	def __init__(self, rucaptcha_key, sleep_time=6, **kwargs):
		self.RUCAPTCHA_KEY = rucaptcha_key
		self.sleep_time = sleep_time
		# пайлоад POST запроса на отправку капчи на сервер
		self.post_payload = {"key": self.RUCAPTCHA_KEY,
							 "method": "post",
							 "json": 1,
							 "soft_id": app_key,
							 }
		# Если переданы ещё параметры - вносим их в payload
		if kwargs:
			for key in kwargs:
				self.post_payload.update({key: kwargs[key]})

		# пайлоад GET запроса на получение результата решения капчи
		self.get_payload = {'key': self.RUCAPTCHA_KEY,
							'action': 'get',
							'json': 1,
							}
		# результат возвращаемый методом *captcha_handler*
		# в captchaSolve - решение капчи,
		# в taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
		# в errorId - 0 - если всё хорошо, 1 - если есть ошибка,
		# в errorBody - тело ошибки, если есть.
		self.result = {"captchaSolve": None,
					   "taskId": None,
					   "errorId": None,
					   "errorBody": None
					   }

	def captcha_handler(self, captcha_text):
		# Создаём пайлоад, вводим ключ от сайта, выбираем метод ПОСТ и ждём ответа. в JSON-формате
		self.post_payload.update({"textcaptcha": captcha_text})
		# Отправляем на рукапча текст капчи и ждём ответа
		#  в результате получаем JSON ответ с номером решаемой капчи
		captcha_id = requests.post(url_request,
									data=self.post_payload).json()

		# если вернулся ответ с ошибкой то записываем её и возвращаем результат
		if captcha_id['status'] is 0:
			self.result.update({'errorId': 1,
								'errorBody': RuCaptchaError().errors(captcha_id['request'])
								}
							   )
			return self.result
		# иначе берём ключ отправленной на решение капчи и ждём решения
		else:
			captcha_id = captcha_id['request']
			# вписываем в taskId ключ отправленной на решение капчи
			self.result.update({"taskId": captcha_id})
			# обновляем пайлоад, вносим в него ключ отправленной на решение капчи
			self.get_payload.update({'id': captcha_id})

		# Ожидаем решения капчи
		time.sleep(self.sleep_time)
		while True:
			# отправляем запрос на результат решения капчи, если не решена ожидаем
			captcha_response = requests.post(url_response, data = self.get_payload)

			# если капча ещё не решена - ожидаем
			if captcha_response.json()['request'] == 'CAPCHA_NOT_READY':
				time.sleep(self.sleep_time)

			# при ошибке во время решения
			elif captcha_response.json()["status"] == 0:
				self.result.update({'errorId': 1,
									'errorBody': RuCaptchaError().errors(captcha_response.json()["request"])
									}
								   )
				return self.result

			# при решении капчи
			elif captcha_response.json()["status"] == 1:
				self.result.update({'errorId': 0,
									'captchaSolve': captcha_response.json()['request']
									}
								   )
				return self.result

