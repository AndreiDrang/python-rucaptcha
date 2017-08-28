import requests
from python_rucaptcha import ImageCaptcha


"""
Этот пример показывает то как нужно работать с модулем для распознования обычной капчи изображением,
на примере нашего сайта.
В общем случае вам потребуется получение:
1. Получить ссылку на изображение капчи(сртрока 14 в примере)
2. Передать эту ссылку в модуль ImageCaptcha(строка 19 в примере)
"""
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = ""
# Для получения ссылки на обычную капчу нужно послать гет запрос с соответствующим парметром
captcha_link = requests.get("http://85.255.8.26/api/", params={"captcha_type":"get_common_captcha"}).json()["captcha_src"]
"""
Тут нужно воспользоваться бибилотекой, отослать на решение ссылку на капчу и получить ответ
далее его записать в user_answer и отправить на проверку уже на наш сайт
"""
user_answer = ImageCaptcha.ImageCaptcha(recaptcha_api=RUCAPTCHA_KEY).captcha_handler(captcha_link=captcha_link)

# Вычленяем из ссылки название капчи
captcha_name = captcha_link.split("/")[-1]
# Для проверки правильности разгадки капчи нужно послать ПОСТ запрос c именем капчи и ответом юзера
server_answer = requests.post("http://85.255.8.26/api/", data={"common_captcha_src":captcha_name,
	                                                         "common_captcha_answer":user_answer,
	                                                         "common_captcha_btn": True})
# Есть два типа ответа: OK и FAIL
print(server_answer.json()["request"])