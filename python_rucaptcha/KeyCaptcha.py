import requests
import time

from .config import url_request, url_response, app_key
from .errors import RuCaptchaError

class KeyCaptcha:
	
	def __init__(self, rucaptcha_key, key_captcha_data, sleep_time=5):
		self.s_s_c_user_id = key_captcha_data['s_s_c_user_id']
		self.s_s_c_session_id = key_captcha_data['s_s_c_session_id']
		self.s_s_c_web_server_sign = key_captcha_data['s_s_c_web_server_sign']
		self.s_s_c_web_server_sign2 = key_captcha_data['s_s_c_web_server_sign2']
		self.page_url = key_captcha_data['page_url']
		
		self.RUCAPTCHA_KEY = rucaptcha_key
		self.sleep_time = sleep_time


	def captcha_handler(self):
		captcha_id = (requests.post(url_request+"""?key={0}&
													s_s_c_user_id={1}&s_s_c_session_id={2}&
									            	s_s_c_web_server_sign={3}&s
									            	_s_c_web_server_sign2={4}&
									            	method=keycaptcha&pageurl={5}&j
									            	son=1&
									            	soft_id={6}"""
		                                    .format(self.RUCAPTCHA_KEY,
													self.s_s_c_user_id,
													self.s_s_c_session_id,
		                                            self.s_s_c_web_server_sign,
													self.s_s_c_web_server_sign2,
		                                            self.page_url,
													app_key)
									).json())

		if captcha_id['status'] is 0:
			return RuCaptchaError(captcha_id['request'])

		captcha_id = captcha_id['request']

		# Ожидаем решения капчи
		time.sleep(self.sleep_time)
		while True:
			# отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
			# если всё ок - идём дальше
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