import httplib2
import requests

class SolvingTextCaptcha:
	def __init__(self, recaptcha_api, sleep_time = 6):
		self.url_request = "http://2captcha.com/in.php"
        self.url_response = "http://2captcha.com/res.php"
        self.RECAPTCHA_KEY = recaptcha_api
        self.sleep_time = sleep_time
	
	def handle_captcha(self):
		pass