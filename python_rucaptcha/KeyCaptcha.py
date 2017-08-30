import requests
import time

from config import url_request, url_response, app_key
from errors import RuCaptchaError

class KeyCaptcha:
	
	def __init__(self, rucaptcha_key, key_captcha_data, sleep_time=5):
		self.s_s_c_user_id = key_captcha_data['s_s_c_user_id']
		self.s_s_c_session_id = key_captcha_data['s_s_c_session_id']
		self.s_s_c_web_server_sign = key_captcha_data['s_s_c_web_server_sign']
		self.s_s_c_web_server_sign2 = key_captcha_data['s_s_c_web_server_sign2']
		self.page_url = key_captcha_data['page_url']
		
		self.RECAPTCHA_KEY = rucaptcha_key
		self.sleep_time = sleep_time


	def captcha_handler(self):
		captcha_id = (requests.post(url_request+"""?key={0}&s_s_c_user_id={1}&s_s_c_session_id={2}&
									            s_s_c_web_server_sign={3}&s_s_c_web_server_sign2={4}&
									            method=keycaptcha&pageurl={5}&json=1&soft_id={6}"""
		                                        .format(self.RECAPTCHA_KEY, self.s_s_c_user_id, self.s_s_c_session_id,
		                                                self.s_s_c_web_server_sign, self.s_s_c_web_server_sign2,
		                                                self.page_url, app_key)
									).json())['request']

		# Ожидаем решения капчи
		time.sleep(self.sleep_time)
		while True:
			# отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
			# если всё ок - идём дальше
			captcha_response = requests.request('GET',
			                                    url_response + "?key={0}&action=get&id={1}&json=1"
			                                    .format(self.RECAPTCHA_KEY, captcha_id))
			if captcha_response.json()["request"] == 'CAPCHA_NOT_READY':
				time.sleep(self.sleep_time)
			else:
				return captcha_response.json()['request']


