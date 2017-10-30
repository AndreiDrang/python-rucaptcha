import requests
import time
import tempfile

from .config import url_request, url_response, app_key
from .errors import RuCaptchaError


class RotateCaptcha:
    def __init__(self, rucaptcha_key, sleep_time=5):
        '''
        Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удалются временные фалйы и папки
        :param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
        '''

        self.sleep_time = sleep_time
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             'method': 'rotatecaptcha',
                             "json": 1,
                             "soft_id": app_key}

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': rucaptcha_key,
                            'action': 'get',
                            'json': 1,
                            }
        # результат возвращаемый методом *captcha_handler*
        # в captchaSolve - решение капчи,
        # в taskId - находится Id задачи на решение капчи, можно использовать при жалобах и прочем,
        # в errorId - 0 - если всё хорошо, 1 - если есть ошибка,
        # в errorBody - тело ошибки, если есть.
        self.result = {"captchaSolve": None,
                       "taskId": None,
                       "errorId": None,
                       "errorBody": None
                       }

    # Работа с капчёй
    def captcha_handler(self, captcha_link):
        '''
        Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
        :return: Ответ на капчу
        '''
        # Скачиваем изображение
        content = requests.get(captcha_link).content
        with tempfile.NamedTemporaryFile(suffix='.jpg') as out:
            out.write(content)
            captcha_image = open(out.name, 'rb')
            # Отправляем изображение файлом
            files = {'file': captcha_image}
            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            captcha_id = requests.request('POST', url_request, data=self.post_payload, files=files).json()

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id['status'] is 0:
            self.result.update({'errorId': 1,
                                'errorBody': RuCaptchaError().errors(captcha_id['request'])
                                }
                               )
            return self.result
        # иначе берём ключ отправленной на решение капчи и ждём решения
        else:
            captcha_id = captcha_id['request']
            # вписываем в taskId ключ отправленной на решение капчи
            self.result.update({"taskId": captcha_id})
            # обновляем пайлоад, вносим в него ключ отправленной на решение капчи
            self.get_payload.update({'id': captcha_id})

        # Ожидаем решения капчи 20 секунд
        time.sleep(self.sleep_time)

        while True:
            # отправляем запрос на результат решения капчи, если не решена ожидаем
            captcha_response = requests.post(url_response, data=self.get_payload)
    
            # если капча ещё не решена - ожидаем
            if captcha_response.json()['request'] == 'CAPCHA_NOT_READY':
                time.sleep(self.sleep_time)
    
            # при ошибке во время решения
            elif captcha_response.json()["status"] == 0:
                self.result.update({'errorId': 1,
                                    'errorBody': RuCaptchaError().errors(captcha_response.json()["request"])
                                    }
                                   )
                return self.result
    
            # при решении капчи
            elif captcha_response.json()["status"] == 1:
                self.result.update({'errorId': 0,
                                    'captchaSolve': captcha_response.json()['request']
                                    }
                                   )
                return self.result

