import requests
import CommonCaptcha


# Введите ключ от рукапчи
RECAPTCHA_KEY = ""
# Для получения ссылки на обычную капчу нужно послать гет запрос с соответствующим парметром
captcha_link = requests.get("http://127.0.0.1:5000/", params={"captcha_type":"get_common_captcha"}).json()["captcha_src"]
"""
Тут нужно воспользоваться бибилотекой, отослать на решение ссылку на капчу и получить ответ
далее его записать в user_answer и отправить на проверку уже на наш сайт
"""
user_answer = CommonCaptcha.CommonCaptcha(recaptcha_api=RECAPTCHA_KEY).captcha_handler(captcha_link=captcha_link)

# Вычленяем из ссылки название капчи
captcha_name = captcha_link.split("/")[-1]
# Для проверки правильности разгадки капчи нужно послать ПОСТ запрос c именем капчи и ответом юзера
server_answer = requests.post("http://127.0.0.1:5000/", data={"common_captcha_src":captcha_name,
	                                                         "common_captcha_answer":user_answer,
	                                                         "common_captcha_btn": True})
# Есть два типа ответа: OK и FAIL
print(server_answer.json()["request"])