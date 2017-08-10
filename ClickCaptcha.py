import requests
import os, shutil
import hashlib
import httplib2
import time


class ClickCaptcha:
	
	def __init__(self, recaptcha_api, sleep_time=5):
		self.RECAPTCHA_KEY = recaptcha_api
		self.sleep_time = sleep_time
		self.img_path = os.path.normpath('click_images')
		#создать папку для сохранения картинок
		
		try:
			if not os.path.exists(self.img_path):
				os.mkdir(self.img_path)
			if not os.path.exists(".cache"):
				os.mkdir(".cache")
		except Exception as err:
			print(err)


	def captcha_handler(self, captcha_link):
		#получить изображение и инструкцию
		
		#сохранение изображения
		image_hash = hashlib.sha224(captcha_link.encode('utf-8')).hexdigest()
		cache = httplib2.Http(".cache")
		response, content = cache.request(captcha_link)
		out = open(os.path.join(self.img_path, 'img-{0}.jpg'.format(image_hash)), 'wb')
		out.write(content)
		out.close()

		with open(os.path.join(self.img_path, "img-{0}.jpg".format(image_hash)), 'rb') as captcha_image:
			files = {"file": captcha_image}
			#отправить запрос POST к http://rucaptcha.com/in.php c параметром coordiantescaptcha=1
			payload = {"key": self.RECAPTCHA_KEY, 
						"method": "post", 
						"textinstructions": "!instructions example!",
						"coordinatecaptcha": 1, 
						"json": 1}
			#получить ID капчи или код ошибки
			captcha_id = (requests.request("POST",
											"http://rucaptcha.com/in.php",
											data=payload,
											files=files).json())["request"]
			print(captcha_id)
		#удаляем временные файлы и картинку
		#os.remove(os.path.join(self.img_path, "img-{0}.jpg".format(image_hash)))
		#ждем 5 секунд
		time.sleep(self.sleep_time * 4)
		
		while True:
			#отправляем запрос на результат решения капчи
			captcha_response = requests.request("GET",
												"http://rucaptcha.com/res.php?key={0}&action=get&id={1}&json=1".
												format(self.RECAPTCHA_KEY, captcha_id))
			#если капча решена, сервер вернет координаты точек по которым нужно кликнуть
			if captcha_response.json()["request"] == 'CAPTCHA_NOT_READY':
				time.sleep(6)
			else:
				return captcha_response.json()["request"]


	def __del__(self):
		if os.path.exists("click_images"):
			shutil.rmtree("click_images")
		if os.path.exists(".cache"):
			shutil.rmtree(".cache")