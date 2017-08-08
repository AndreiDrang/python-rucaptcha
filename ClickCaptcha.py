import requests
import os
class ClickCaptcha:
	
	def __init__(self, recaptcha_api, sleep_time=5):
		self.RECAPTCHA_KEY = recaptcha_api
		self.sleep_time = sleep_time
		self.img_path = os.path.normpath('click_images')
		#создать папку для сохранения картинок
		
		try:
			if not os.path.exists(self.img_path):
				os.mkdir(self.img_path)
		except Exception as err:
			print(err)


	def captcha_handler(self):
		pass
		#получить изображение и инструкцию
		#отправить запрос POST к http://rucaptcha.com/in.php c параметром coordiantescaptcha=1
		#получить ID капчи или код ошибки
		#ждем 5 секунд
		#отправляем запрос GET к http://rucaptcha.com/res.ph чтобы получить результат
		#если капча решена, сервер вернет координаты точек по которым нужно кликнуть