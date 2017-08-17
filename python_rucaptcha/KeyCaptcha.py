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
		
		self.RECAPTCHA_KEY = recaptcha_api
		self.sleep_time = sleep_time
		try:
			if not os.path.exists(self.img_path):
				os.mkdir(self.img_path)
			if not os.path.exists(".cache"):
				os.mkdir(".cache")
		except Exception as err:
			print(err)
	

	def captcha_handler(self, captcha_link):

		
		# Высчитываем хэш изображения, для того что бы сохранить его под уникальным именем
		image_hash = hashlib.sha224(captcha_link.encode('utf-8')).hexdigest()
		# Скачиваем изображение и сохраняем на диск в папку images
		cache = httplib2.Http('.cache')
		response, content = cache.request(captcha_link)
		out = open(os.path.join(self.img_path, 'im-{0}.jpg'.format(image_hash)), 'wb')
		out.write(content)
		out.close()
		
		with open(os.path.join(self.img_path, 'im-{0}.jpg'.format(image_hash)), 'rb') as captcha_image:
			# Отправляем изображение файлом
			files = {'file': captcha_image}
			# Создаём пайлоад, вводим ключ от сайта, выбираем метод ПОСТ и ждём ответа в JSON-формате
			payload = {"key": self.RECAPTCHA_KEY,
			           "method": "post",
			           "json": 1,
			           "soft_id": app_key}
			# Отправляем на рукапча изображение капчи и другие парметры,
			# в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
			captcha_id = (requests.request('POST',
			                               url_request,
			                               data=payload,
			                               files=files).json())['request']
		
		# удаляем файл капчи и врменные файлы
		os.remove(os.path.join(self.img_path, "im-{0}.jpg".format(image_hash)))
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
	
	def __del__(self):
		if os.path.exists(".cache"):
			shutil.rmtree(".cache")