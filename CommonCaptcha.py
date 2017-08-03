import httplib2
import requests
import os, shutil
import time, datetime

class CommonCaptcha:
    def __init__(self, recaptcha_api, sleep_time = 5):
        self.url_request = "http://2captcha.com/in.php"
        self.url_response = "http://2captcha.com/res.php"
        self.RECAPTCHA_KEY = recaptcha_api
        self.sleep_time = sleep_time

        try:
            if not os.path.exists("common_captcha_images"):
                os.mkdir("common_captcha_images")
            if not os.path.exists(".cache"):
                os.mkdir(".cache")
        except Exception as err:
            print(err)

    # Работа с капчёй
    def captcha_handler(self, captcha_link):
        # Скачиваем изображение и сохраняем на диск в папку images
        cache = httplib2.Http('.cache')
        response, content = cache.request(captcha_link)
        out = open('images\{0}.jpg'.format(captcha_link), 'wb')
        out.write(content)
        out.close()

        with open('images\{0}.jpg'.format(captcha_link), 'rb') as captcha_image:
            # Отправляем изображение файлом
            files = {'file': captcha_image}
            # Создаём пайлоад, вводим ключ от сайта, выбираем метод ПОСТ и ждём ответа в JSON-формате
            payload = {"key": self.RECAPTCHA_KEY,
                       "method": "post",
                       "json": 1}
            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            captcha_id = (requests.request('POST',
                                           "http://rucaptcha.com/in.php",
                                           data=payload,
                                           files=files).json())['request']

        # удаляем файл капчи и врменные файлы
        os.remove("images\{0}.jpg".format(captcha_link))
        # Ожидаем решения капчи
        time.sleep(5)
        while True:
            # отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
            # если всё ок - идём дальше
            captcha_response = requests.request('GET',
                                                "http://rucaptcha.com/res.php?key={0}&action=get&id={1}&json=1"
                                                .format(self.RECAPTCHA_KEY, captcha_id))
            if captcha_response.json()["request"] == 'CAPCHA_NOT_READY':
                time.sleep(self.sleep_time)
            else:
                return (captcha_response.json())['request']

    def __del__(self):
        if os.path.exists("common_captcha_images"):
            shutil.rmtree("common_captcha_images")
        if os.path.exists(".cache"):
            shutil.rmtree(".cache")
