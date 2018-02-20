import requests
import time

from .config import url_request, url_response, app_key
from .errors import RuCaptchaError

class KeyCaptcha:
	
	def __init__(self, rucaptcha_key, sleep_time=5):
		self.RUCAPTCHA_KEY = rucaptcha_key
		self.sleep_time = sleep_time
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
		               "errorBody": None}

	def captcha_handler(self, **kwargs):
		# считываем все переданные параметры KeyCaptcha
		try:
			self.s_s_c_user_id = kwargs['s_s_c_user_id']
			self.s_s_c_session_id = kwargs['s_s_c_session_id']
			self.s_s_c_web_server_sign = kwargs['s_s_c_web_server_sign']
			self.s_s_c_web_server_sign2 = kwargs['s_s_c_web_server_sign2']
			self.page_url = kwargs['page_url']
		except KeyError as error:
			self.result.update({'errorId': 1,
			                    'errorBody': error
			                    }
			                   )
			return self.result
		
		# передаём параметры кей капчи для решения
		captcha_id = requests.post(url=url_request, json={'key':self.RUCAPTCHA_KEY,
		                                                  's_s_c_user_id':self.s_s_c_user_id,
		                                                  's_s_c_session_id':self.s_s_c_session_id,
		                                                  's_s_c_web_server_sign':self.s_s_c_web_server_sign,
		                                                  's_s_c_web_server_sign2':self.s_s_c_web_server_sign2,
		                                                  'method':'keycaptcha',
		                                                  'pageurl': self.page_url,
		                                                  'json':1,
		                                                  'soft_id':app_key}).json()
		
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
			
			# отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
			# если всё ок - идём дальше
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
					
				# при ошибке решения - пораждаем исключение
				elif captcha_response.json()["status"] == 0:
					self.result.update({'errorId': 1,
					                    'errorBody': RuCaptchaError().errors(captcha_response.json()["request"])
					                    }
					                   )
					return self.result
				
				# если капча решена - возвращаем ответ
				elif captcha_response.json()["status"] == 1:
					self.result.update({'errorId': 0,
					                    'captchaSolve': captcha_response.json()['request']
					                    }
					                   )
					return self.result