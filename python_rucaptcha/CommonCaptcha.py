import httplib2
import requests
import os, shutil
import tempfile
import time
import hashlib
from config import url_request, url_response

class CommonCaptcha:
    '''
    Данный метод подходит как для загрузки и решения обычной капчи
    так и для большой капчи.
    Требуется передать API ключ сайта, ссылку на изображение и,по желанию, время ожидания решения капчи
    Подробней информацию смотрите в методе 'captcha_handler'
    '''
    
    def __init__(self, recaptcha_api, sleep_time=5):
        '''
        Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удалются временные фалйы и папки
        :param recaptcha_api:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
        '''
        self.RECAPTCHA_KEY = recaptcha_api
        self.sleep_time = sleep_time
        self.temp = tempfile.TemporaryFile(mode='w+b',
                                                prefix='img-',
                                                suffix='.jpg')
        self.img_path = os.path.normpath('common_captcha_images')
        try:
            if not os.path.exists(self.img_path):
                os.mkdir(self.img_path)
            if not os.path.exists(".cache"):
                os.mkdir(".cache")
        except Exception as err:
            print(err)

    # Работа с капчёй
    def captcha_handler(self, captcha_link):
        '''
        Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
        :return: Ответ на капчу
        '''

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
                       "json": 1}
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
                                                url_response+"?key={0}&action=get&id={1}&json=1"
                                                .format(self.RECAPTCHA_KEY, captcha_id))
            if captcha_response.json()["request"] == 'CAPCHA_NOT_READY':
                time.sleep(self.sleep_time)
            else:
                return captcha_response.json()['request']

    def __del__(self):
        if os.path.exists(".cache"):
            shutil.rmtree(".cache")

