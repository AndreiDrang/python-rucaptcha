import requests
import time
import asyncio
import aiohttp
from requests.adapters import HTTPAdapter

from .config import url_request_2captcha, url_response_2captcha, url_request_rucaptcha, url_response_rucaptcha, app_key, \
    JSON_RESPONSE, connect_generator
from .errors import RuCaptchaError


class ReCaptchaV2:
    """
	Класс служит для работы с новой ReCaptcha от Гугла и Invisible ReCaptcha.
	Для работы потребуется передать ключ от РуКапчи, затем ключ сайта(подробности его получения в описании на сайте)
	И так же ссылку на сайт.
	"""

    def __init__(self, rucaptcha_key, service_type: str = '2captcha', sleep_time: int = 10, invisible: int = 0,
                 proxy: str = '', proxytype: str = ''):
        """
		Инициализация нужных переменных.
		:param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
		:param sleep_time: Вермя ожидания решения капчи
		:param proxy: Для решения рекапчи через прокси - передаётся прокси и данные для аутентификации.
		                ` логин:пароль@IP_адрес:ПОРТ` / `login:password@IP:port`.
		:param proxytype: Тип используемого прокси. Доступные: `HTTP`, `HTTPS`, `SOCKS4`, `SOCKS5`.
		:param invisible: Для решения невидимой ReCaptcha нужно выставить параметр 1
		"""
        # проверка введённого времени и изменение если минимальный порог нарушен
        if sleep_time < 10:
            raise ValueError(f'\nПараметр `sleep_time` должен быть не менее 10(рекомендуемое - 20 секунд). '
                             f'\n\tВы передали - {sleep_time}')
        self.sleep_time = sleep_time
        # проверка допустимости переданного параметра для невидимой/обыкновенной капчи
        if invisible not in (0, 1):
            raise ValueError(f'\nПараметр `invisible` может быть равен 1 или 0. \n\tВы передали - {invisible}')
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             'method': 'userrecaptcha',
                             "json": 1,
                             'invisible': invisible,
                             "soft_id": app_key}

        # добавление прокси для решения капчи с того же IP
        if proxy and proxytype:
            self.post_payload.update({'proxy': proxy,
                                      'proxytype': proxytype})

        # выбираем URL на который будут отпраляться запросы и с которого будут приходить ответы
        if service_type == '2captcha':
            self.url_request = url_request_2captcha
            self.url_response = url_response_2captcha
        elif service_type == 'rucaptcha':
            self.url_request = url_request_rucaptcha
            self.url_response = url_response_rucaptcha
        else:
            raise ValueError('Передан неверный параметр URL-сервиса капчи! Возможные варинты: `rucaptcha` и `2captcha`.'
                             'Wrong `service_type` parameter. Valid formats: `rucaptcha` or `2captcha`.')

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': rucaptcha_key,
                            'action': 'get',
                            'json': 1,
                            }

        # создаём сессию
        self.session = requests.Session()
        # выставляем кол-во попыток подключения к серверу при ошибке
        self.session.mount('http://', HTTPAdapter(max_retries = 5))
        self.session.mount('https://', HTTPAdapter(max_retries = 5))

    # Работа с капчей
    # тестовый ключ сайта
    def captcha_handler(self, site_key: str, page_url: str):
        '''
		Метод отвечает за передачу данных на сервер для решения капчи
		:param site_key: Гугл-ключ сайта
		:param page_url: Ссылка на страницу на которой находится капча
		:return: В качестве ответа переждаётся строка которую нужно вставить для отправки гуглу на проверку
		'''
        # результат возвращаемый методом *captcha_handler*
        self.result = JSON_RESPONSE.copy()
        # генератор для повторных попыток подключения к серверу получения решения капчи
        self.connect_gen = connect_generator()

        self.post_payload.update({'googlekey': site_key,
                                  'pageurl': page_url})
        # получаем ID капчи
        captcha_id = self.session.post(self.url_request, data = self.post_payload).json()

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id['status'] is 0:
            self.result.update({'error': True,
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

        # Ожидаем решения капчи 10 секунд
        time.sleep(self.sleep_time)
        while True:
            try:
                # отправляем запрос на результат решения капчи, если не решена ожидаем
                captcha_response = requests.post(self.url_response, data = self.get_payload)
                # если капча ещё не решена - ожидаем
                if captcha_response.json()['request'] == 'CAPCHA_NOT_READY':
                    time.sleep(self.sleep_time)

                # при ошибке во время решения
                elif captcha_response.json()["status"] == 0:
                    self.result.update({'error': True,
                                        'errorBody': RuCaptchaError().errors(captcha_response.json()["request"])
                                        }
                                       )
                    return self.result

                # при решении капчи
                elif captcha_response.json()["status"] == 1:
                    self.result.update({
                                        'captchaSolve': captcha_response.json()['request']
                                        }
                                       )
                    return self.result

            except Exception as error:
                if next(self.connect_gen) < 4:
                    time.sleep(2)
                else:
                    self.result.update({'error': True,
                                        'errorBody': {
                                            'text': error,
                                            'id': -1
                                        }
                                        }
                                       )
                    return self.result


# асинхронный метод для решения РеКапчи 2
class aioReCaptchaV2:
    """
	Класс служит для асинхронной работы с новой ReCaptcha от Гугла и Invisible ReCaptcha.
	Для работы потребуется передать ключ от РуКапчи, затем ключ сайта(подробности его получения в описании на сайте)
	И так же ссылку на сайт.
	"""

    def __init__(self, rucaptcha_key: str, service_type: str = '2captcha', sleep_time: int = 10, invisible: int = 0, proxy: str = '',
                 proxytype: str = ''):
        """
		Инициализация нужных переменных.
		:param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
		:param sleep_time: Время ожидания решения капчи
		:param proxy: Для решения рекапчи через прокси - передаётся прокси и данные для аутентификации.
		                ` логин:пароль@IP_адрес:ПОРТ` / `login:password@IP:port`.
		:param proxytype: Тип используемого прокси. Доступные: `HTTP`, `HTTPS`, `SOCKS4`, `SOCKS5`.
		:param invisible: Для решения невидимой ReCaptcha нужно выставить параметр 1
		"""
        if sleep_time < 10:
            raise ValueError(f'Параметр `sleep_time` должен быть не менее 10. Вы передали - {sleep_time}')
        self.sleep_time = sleep_time
        # проверка допустимости переданного параметра для невидимой/обыкновенной капчи
        if invisible not in (0, 1):
            raise ValueError(f'\nПараметр `invisible` может быть равен 1 или 0. \n\tВы передали - {invisible}')
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             'method': 'userrecaptcha',
                             "json": 1,
                             'invisible': invisible,
                             "soft_id": app_key
                             }

        # добавление прокси для решения капчи с того же IP
        if proxy and proxytype:
            self.post_payload.update({'proxy': proxy,
                                      'proxytype': proxytype})

        # выбираем URL на который будут отпраляться запросы и с которого будут приходить ответы
        if service_type == '2captcha':
            self.url_request = url_request_2captcha
            self.url_response = url_response_2captcha
        elif service_type == 'rucaptcha':
            self.url_request = url_request_rucaptcha
            self.url_response = url_response_rucaptcha
        else:
            raise ValueError('Передан неверный параметр URL-сервиса капчи! Возможные варинты: `rucaptcha` и `2captcha`.'
                             'Wrong `service_type` parameter. Valid formats: `rucaptcha` or `2captcha`.')

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': rucaptcha_key,
                            'action': 'get',
                            'json': 1,
                            }

    # Работа с капчей
    async def captcha_handler(self, site_key: str, page_url: str):
        '''
		Метод отвечает за передачу данных на сервер для решения капчи
		:param site_key: Гугл-ключ сайта
		:param page_url: Ссылка на страницу на которой находится капча
		:return: В качестве ответа переждаётся строка которую нужно вставить для отправки гуглу на проверку
		'''
        # результат возвращаемый методом *captcha_handler*
        self.result = JSON_RESPONSE.copy()
        # генератор для повторных попыток подключения к серверу получения решения капчи
        self.connect_gen = connect_generator()

        self.post_payload.update({'googlekey': site_key, 'pageurl': page_url})
        # получаем ID капчи
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url_request, data = self.post_payload) as resp:
                captcha_id = await resp.json()

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id['status'] is 0:
            self.result.update({'error': True,
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

        # Ожидаем решения капчи
        await asyncio.sleep(self.sleep_time)
        # отправляем запрос на результат решения капчи, если не решена ожидаем
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.post(self.url_response, data = self.get_payload) as resp:
                        captcha_response = await resp.json()

                        # если капча ещё не решена - ожидаем
                        if captcha_response['request'] == 'CAPCHA_NOT_READY':
                            await asyncio.sleep(self.sleep_time)

                        # при ошибке во время решения
                        elif captcha_response["status"] == 0:
                            self.result.update({'error': True,
                                                'errorBody': RuCaptchaError().errors(captcha_response["request"])
                                                }
                                               )
                            return self.result

                        # при решении капчи
                        elif captcha_response["status"] == 1:
                            self.result.update({
                                                'captchaSolve': captcha_response['request']
                                                }
                                               )
                            return self.result

                except Exception as error:
                    if next(self.connect_gen) < 4:
                        time.sleep(2)
                    else:
                        self.result.update({'error': True,
                                            'errorBody': {
                                                'text': error,
                                                'id': -1
                                            }
                                            }
                                           )
                        return self.result
