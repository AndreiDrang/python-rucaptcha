import requests
import time
import asyncio
import aiohttp

from .config import url_request, url_response, app_key
from .errors import RuCaptchaError


class ReCaptchaV2:
	"""
	Класс служит для работы с новой ReCaptcha от Гугла и Invisible ReCaptcha.
	Для работы потребуется передать ключ от РуКапчи, затем ключ сайта(подробности его получения в описании на сайте)
	И так же ссылку на сайт.
	"""

	def __init__(self, rucaptcha_key, sleep_time = 16):
		"""
		Инициализация нужных переменных.
		:param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
		:param sleep_time: Вермя ожидания решения капчи
		"""
		self.RUCAPTCHA_KEY = rucaptcha_key
		self.sleep_time = sleep_time
		# пайлоад POST запроса на отправку капчи на сервер
		self.post_payload = {"key": self.RUCAPTCHA_KEY,
							 'method': 'userrecaptcha',
							 "json": 1,
							 "soft_id": app_key}

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

	# Работа с капчей
	# тестовый ключ сайта
	def captcha_handler(self, site_key, page_url):
		'''
		Метод отвечает за передачу данных на сервер для решения капчи
		:param site_key: Гугл-ключ сайта
		:param page_url: Ссылка на страницу на которой находится капча
		:return: В качестве ответа переждаётся строка которую нужно вставить для отправки гуглу на проверку
		'''
		self.post_payload.update({'googlekey': site_key, 'pageurl': page_url})
		# получаем ID капчи
		captcha_id = requests.post(url_request, data = self.post_payload).json()

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

		# Ожидаем решения капчи 20 секунд
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


class aioReCaptchaV2:
	"""
	Класс служит для асинхронной работы с новой ReCaptcha от Гугла и Invisible ReCaptcha.
	Для работы потребуется передать ключ от РуКапчи, затем ключ сайта(подробности его получения в описании на сайте)
	И так же ссылку на сайт.
	"""

	def __init__(self, rucaptcha_key, sleep_time = 10):
		"""
		Инициализация нужных переменных.
		:param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
		:param sleep_time: Вермя ожидания решения капчи
		"""
		self.sleep_time = sleep_time
		# пайлоад POST запроса на отправку капчи на сервер
		self.post_payload = {"key": rucaptcha_key,
							 'method': 'userrecaptcha',
							 "json": 1,
							 "soft_id": app_key
							 }

		# пайлоад GET запроса на получение результата решения капчи
		self.get_payload = {'key': rucaptcha_key,
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

	# Работа с капчей
	async def captcha_handler(self, site_key, page_url):
		'''
		Метод отвечает за передачу данных на сервер для решения капчи
		:param site_key: Гугл-ключ сайта
		:param page_url: Ссылка на страницу на которой находится капча
		:return: В качестве ответа переждаётся строка которую нужно вставить для отправки гуглу на проверку
		'''
		self.post_payload.update({'googlekey': site_key, 'pageurl': page_url})
		# получаем ID капчи
		async with aiohttp.ClientSession() as session:
			async with session.post(url_request, data = self.post_payload) as resp:
				captcha_id = await resp.json()

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
		await asyncio.sleep(self.sleep_time)
		# отправляем запрос на результат решения капчи, если не решена ожидаем
		async with aiohttp.ClientSession() as session:
			while True:
				async with session.post(url_response, data = self.get_payload) as resp:
					captcha_response = await resp.json()

					# если капча ещё не решена - ожидаем
					if captcha_response['request'] == 'CAPCHA_NOT_READY':
						await asyncio.sleep(self.sleep_time)

					# при ошибке во время решения
					elif captcha_response["status"] == 0:
						self.result.update({'errorId': 1,
											'errorBody': RuCaptchaError().errors(captcha_response["request"])
											}
										   )
						return self.result

					# при решении капчи
					elif captcha_response["status"] == 1:
						self.result.update({'errorId': 0,
											'captchaSolve': captcha_response['request']
											}
										   )
						return self.result

