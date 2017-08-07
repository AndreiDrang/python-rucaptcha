import requests
import time
# Checking captcha
def captcha():
    captcha_download = 'http://rucaptcha.com/in.php?key={0}&method=userrecaptcha&googlekey={1}'\
        .format(recaptcha_key,site_key)
    # then i have answer like: OK|CAPTCHA_ID
    # checking captcha
    http = urllib3.PoolManager()
    answer = http.request('GET', captcha_download)
    # get captcha ID
    captcha_id = (str(answer.data).split('|'))[1]
    answer = 'http://rucaptcha.com/res.php?key={0}&action=get&id={1}'.format(recaptcha_key, captcha_id)
    # get answer on captcha
    time.sleep(13)
    while True:
        captcha_response = requests.request('GET', answer)
        if str(captcha_response.content) == 'CAPCHA_NOT_READY':
            time.sleep( 5 )
        else:
            answer = (str(captcha_response.content).split('|'))[1]
            break
    return answer


class ReCaptcha:
	def __init__(self, recaptcha_api, sleep_time=5):
		self.url_request = "http://2captcha.com/in.php"
        self.url_response = "http://2captcha.com/res.php"
        self.RECAPTCHA_KEY = recaptcha_api
        self.sleep_time = sleep_time

    #Работа с капчей
	def handle_captcha(self):
		pass