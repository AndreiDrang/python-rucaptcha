import httplib2
import requests
import os, shutil
import tempfile
import time
import hashlib
from config import url_request, url_response, app_key


class KeyCaptcha:
	
	def __init__(self, recaptcha_api, key_captcha_data, sleep_time=5):
		self.s_s_c_user_id = key_captcha_data['s_s_c_user_id']
		self.s_s_c_session_id = key_captcha_data['s_s_c_session_id']
		self.s_s_c_web_server_sign = key_captcha_data['s_s_c_web_server_sign']
		self.s_s_c_web_server_sign2 = key_captcha_data['s_s_c_web_server_sign2']
		self.page_url = key_captcha_data['page_url']
		
		self.RECAPTCHA_KEY = recaptcha_api
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

data = {
	"s_s_c_user_id": 15,
	"s_s_c_session_id": '6fdf7cb25b2f1dda68741b4d6d13cbc3',
	"s_s_c_web_server_sign": '053e491bc45a535c613c90cdf26b8f72',
	"s_s_c_web_server_sign2": 'ec55f8fb286bcf019c761298003fe059',
	"page_url": 'https://www.keycaptcha.com/signup/',
}
<<<<<<< HEAD
print(KeyCaptcha(recaptcha_api='5b0290c40569c2d322f085deb32b8c91', key_captcha_data=data).captcha_handler())
=======
#print(KeyCaptcha(recaptcha_api='', key_captcha_data=data).captcha_handler())
>>>>>>> dev
