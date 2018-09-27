class RuCaptchaError(Exception):
    """Базовый класс для всех исключений в этом модуле."""
    def errors(self, description):
        """
        Ошибки in.php
        """
        if description == 'ERROR_WRONG_USER_KEY':
            return WrongUserKeyError.answer()
        elif description == 'ERROR_KEY_DOES_NOT_EXIST':
            return NonExistentKeyError.answer()
        elif description == 'ERROR_ZERO_BALANCE':
            return ZeroBalanceError.answer()
        elif description == 'ERROR_PAGEURL':
            return PageUrlError.answer()
        elif description == 'ERROR_NO_SLOT_AVAILABLE':
            return NoSlotsError.answer()
        elif description == 'ERROR_ZERO_CAPTCHA_FILESIZE':
            return ZerroCaptchaSizeError.answer()
        elif description == 'ERROR_TOO_BIG_CAPTCHA_FILESIZE':
            return ToBigCaptchaSizeError.answer()
        elif description == 'ERROR_WRONG_FILE_EXTENSION':
            return WrongCaptchaFormatError.answer()
        elif description == 'ERROR_IMAGE_TYPE_NOT_SUPPORTED':
            return NotSupportedCaptchaTypeError.answer()
        elif description == 'ERROR_UPLOAD':
            return ErrorUploadCaptchaError.answer()
        elif description == 'ERROR_IP_NOT_ALLOWED':
            return IPNotAllowedError.answer()
        elif description == 'IP_BANNED':
            return BannedIPError.answer()
        elif description == 'ERROR_BAD_TOKEN_OR_PAGEURL':
            return BadTokenOrPageurlCaptchaError.answer()
        elif description == 'ERROR_GOOGLEKEY':
            return ErrorGoogleKeyCaptchaError.answer()
        elif description == 'ERROR_CAPTCHAIMAGE_BLOCKED':
            return BlockedimageCaptchaError.answer()
        elif description == 'MAX_USER_TURN':
            return MaxUserTurnCaptchaError.answer()

        # Ошибки res.php
        elif description == 'CAPCHA_NOT_READY':
            return CaptchaNotReadyError.answer()
        elif description == 'ERROR_CAPTCHA_UNSOLVABLE':
            return UnsolvableCaptchaError.answer()
        elif description == 'ERROR_WRONG_ID_FORMAT':
            return WrongCaptchaIDFormatError.answer()
        elif description == 'ERROR_WRONG_CAPTCHA_ID':
            return WrongCaptchaIDError.answer()
        elif description == 'ERROR_BAD_DUPLICATES':
            return BadDuplicatesError.answer()
        elif description == 'REPORT_NOT_RECORDED':
            return ReportNotRecordedError.answer()

        # Error: NNNN
        elif description == 'ERROR: 1001':
            return Number1001Error.answer()
        elif description == 'ERROR: 1002':
            return Number1002Error.answer()
        elif description == 'ERROR: 1003':
            return Number1003Error.answer()
        elif description == 'ERROR: 1004':
            return Number1004Error.answer()
        elif description == 'ERROR: 1005':
            return Number1005Error.answer()


class ReadError(Exception):
    def __init__(self, error):
        Exception.__init__(self, f"\n\tОшибка порождается при невозможности открыть переднный файл!\n\t\t{error}")


class WrongUserKeyError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при неправильном RuCaptcha KEY.
                            Вы указали значение параметра key в неверном формате, ключ должен содержать 32 символа.
                            Прекратите отправку запросов и проверьте ваш ключ API.
                        
                            ERROR_WRONG_USER_KEY - исключение из таблицы.
                            """,
                'id': 10
                }


class NonExistentKeyError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при несуществующем RuCaptcha KEY.
                            Ключ, который вы указали не существует.
                            Прекратите отправку запросов и проверьте ваш ключ API.
                
                            ERROR_KEY_DOES_NOT_EXIST - исключение из таблицы.""",
                'id': 11
                }


class ZeroBalanceError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при отсутствии средств на балансе.
                            На вашем счету недостаточно средств.
                            Прекратите отправку запросов. Пополните баланс вашего счета, чтобы продолжить работу с сервисом.

                            ERROR_ZERO_BALANCE - исключение из таблицы.""",
                'id': 12
                }


class PageUrlError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при неправильном PageUrl.
                            Параметр pagurl не задан в запросе.
   	                        Остановите отправку запросов и измените ваш код, чтобы передавать правильное значение параметра pagurl.

                            ERROR_PAGEURL - исключение из таблицы.""",
                'id': 13
                }


class NoSlotsError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при отсутсвии свободных слотов в очереди на решение ваших капч.
                            Вы можете получить данную ошибку в двух случаях:
                            1. Очередь ваших капч, которые еще не распределены на работников, слишком длинная.
                                Длина очереди зависит от общего числа капч, которые ждут распределения, и может иметь значения от 50 до 100 капч.
                            2. Максимальная ставка, которую вы указали в настройках вашего аккаунта ниже текущей ставки на сервере.
                                Вы можете повысить вашу максимальную ставку.
                            Если вы получили данную ошибку, не отправляйте ваш запрос повторно сразу же после ее получения.
                            Сделайте паузу в 2-3 секунды и попробуйте повторить ваш запрос.ERROR_WRONG_USER_KEY - исключение из таблицы.
                        
                            ERROR_NO_SLOT_AVAILABLE	 - исключение из таблицы.""",
                'id': 14
                }


class ZerroCaptchaSizeError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при некорректной загрузке изображения.
                            Размер вашего изображения менее 100 байт.
                            Проверьте файл изображения.

                            ERROR_ZERO_CAPTCHA_FILESIZE	 - исключение из таблицы.""",
                'id': 15
                }


class ToBigCaptchaSizeError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при некорректной загрузке изображения.
                            Размер вашего изображения более 100 Кбайт.
                            Проверьте файл изображения.
                        
                        
                            ERROR_TOO_BIG_CAPTCHA_FILESIZE	 - исключение из таблицы.""",
                'id': 16
                }


class WrongCaptchaFormatError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при загрузке некорректного изображения.
                            Файл имеет неподдерживаемое расширение.
                            Допустимые расширения: jpg, jpeg, gif, png.
                            Проверьте файл изображения.
                        
                            ERROR_WRONG_FILE_EXTENSION - исключение из таблицы.""",
                'id': 17
                }


class NotSupportedCaptchaTypeError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при загрузке некорректного изображения.
                            Сервер не может опознать тип вашего файла.
                            Проверьте файл изображения.
                        
                            ERROR_IMAGE_TYPE_NOT_SUPPORTED - искючение из таблицы.""",
                'id': 18
                }


class ErrorUploadCaptchaError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при загрузке некорректного изображения.
                            Сервер не может прочитать файл из вашего POST-запроса.
                            Это происходит, если POST-запрос некорректно сформирован в части отправки файла, либо содержит невалидный base64.
                        
                            ERROR_UPLOAD - искючение из таблицы.""",
                'id': 19
                }


class IPNotAllowedError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при запросе к серверу от неразрешённого IP адреса.
                            Запрос отправлен с IP адреса, который не добавлен в список разрешенных вами IP адресов.
                            Проверьте список адресов.
                        
                            ERROR_IP_NOT_ALLOWED - искючение из таблицы.""",
                'id': 20
                }


class BannedIPError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при чрезмерном количестве попыток авторизации с неверным ключём.
                            Ваш IP адрес заблокирован за чрезмерное количество попыток авторизации с неверным ключем авторизации.
                            Для разблокировки обратитесь в службу технической поддержки.
                        
                            IP_BANNED - искючение из таблицы.""",
                'id': 21
                }


class BadTokenOrPageurlCaptchaError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при некорректной паре googlekey и pageurl.
                            Вы можете получить эту ошибку, если отправляете нам ReCaptcha V2. Ошибка возвращается если вы прислали невалидную
                            пару значений googlekey и pageurl. Обычно так бывает, если ReCaptcha подгружается в iframe с другого домена или поддомена.
                        
                            ERROR_BAD_TOKEN_OR_PAGEURL - искючение из таблицы.""",
                'id': 22
                }


class ErrorGoogleKeyCaptchaError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при несуществующем RuCaptcha KEY.
                            Ключ, который вы указали не существует.
                            Прекратите отправку запросов и проверьте ваш ключ API.
                
                            ERROR_KEY_DOES_NOT_EXIST - исключение из таблицы.""",
                'id': 23
                }
    """Исключение порождается при некорректном recaptcha-sitekey.
    Вы можете получить эту ошибку, если отправляете нам ReCaptcha V2. Ошибка возвращается если sitekey в вашем запросе
    пустой или имеет некорректный формат.

    ERROR_GOOGLEKEY - искючение из таблицы.
    """


class BlockedimageCaptchaError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при загрузке некоректного изображения с сайта.
                            Вы отправили изображение, которые помечено в нашей базе данных как нераспознаваемое.
                            Обычно это происходит, если сайт, на котором вы решаете капчу,
                                прекратил отдавать вам капчу и вместо этого выдает изображение с информацией о блокировке.
                            Попробуйте обойти ограничения этого сайта.
                        
                            ERROR_CAPTCHAIMAGE_BLOCKED - искючение из таблицы.""",
                'id': 24
                }


class MaxUserTurnCaptchaError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при большом кол-ве запросов к IN.php.
                            Вы делаете больше 60 обращений к in.php в течение 3 секунд.
                            Ваш ключ API заблокирован на 10 секунд. Блокировка будет снята автоматически
                        
                            MAX_USER_TURN - искючение из таблицы.""",
                'id': 25
                }


# res.php
class CaptchaNotReadyError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при неготовности капчи.
                            Ваша капча еще не решена.
                            Подождите 5 секунд и повторите ваш запрос.
                        
                            CAPCHA_NOT_READY - исключение из таблицы.""",
                'id': 30
                }


class UnsolvableCaptchaError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при невозможности решить капчу.
                            Мы не можем решить вашу капчу - три наших работника не смогли ее решить, либо мы не получили ответ в течении 90 секунд.
                            Мы не спишем с вас деньги за этот запрос.
                            Вы можете попробовать отправить капчу еще раз.
                        
                            ERROR_CAPTCHA_UNSOLVABLE - исключение из таблицы.""",
                'id': 31
                }


class WrongCaptchaIDFormatError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при некорректном формате номера капчи.
                            Вы отправили ID капчи в неправильном формате.
                            ID состоит только из цифр.
                            Проверьте ID вашей капчи или код, который отвечает за получение и отправку ID.
                        
                            ERROR_WRONG_ID_FORMAT - исключение из таблицы.""",
                'id': 32
                }


class WrongCaptchaIDError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при некорректном номере капчи.
                            Вы отправили неверный ID капчи.
                            Проверьте ID вашей капчи или код, который отвечает за получение и отправку ID.
                        
                            ERROR_WRONG_CAPTCHA_ID - исключение из таблицы.""",
                'id': 33
                }


class BadDuplicatesError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при невозможности решить 100% капч.
                            Ошибка возвращается, если вы используете функцию 100% распознавания.
                            Ошибка означает, что мы достигли максимального числа попыток, но требуемое количество совпадений достигнуто не было.
                            Вы можете попробовать отправить вашу капчу еще раз.
                        
                            ERROR_BAD_DUPLICATES - исключение из таблицы.""",
                'id': 34
                }


class ReportNotRecordedError(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Исключение порождается при некорректной загрузке изображения.
                            Ошибка возвращается при отправке жалобы на неверный ответ если вы уже пожаловались на большое количество верно решенных капч.
                            Убедитесь, что вы отправляете жалобы только в случае неправильного решения.
                        
                            REPORT_NOT_RECORDED - исключение из таблицы.""",
                'id': 35
                }


# NNNN
class Number1001Error(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Блокировка на 10 минут.
                            Вы получили 120 ответов ERROR_NO_SLOT_AVAILABLE за одну минуту
                                из-за того, что ваша максимальная ставка ниже, чем текущая ставка на сервере.
                        
                            ERROR: 1001 - искючение из таблицы.""",
                'id': 40
                }


class Number1002Error(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Блокировка на 5 минут.
                            Вы получили 120 ответов ERROR_ZERO_BALANCE за одну минуту из-за того, что на вашем счету недостаточно средств.
                        
                            ERROR: 1002 - искючение из таблицы.""",
                'id': 41
                }


class Number1003Error(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Блокировка на 30 секунд.
                            Вы получаете ответ ERROR_NO_SLOT_AVAILABLE потому что загружаете очень много капч
                                и на сервере скопилась большая очередь из ваших капч, которые не распределены работникам.
                            Вы получили в три раза больше ошибок, чем число капч, которое вы загрузили (но не менее 120 ошибок).
                            Увеличьте тайм-аут, если вы получаете этот код ошибки.
                        
                            ERROR: 1003 - искючение из таблицы.""",
                'id': 42
                }


class Number1004Error(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Блокировка на 10 минут.
                            Ваш IP адрес заблокирован, потому что мы получили 5 запросов с некорректным ключем API с вашего IP.
                        
                            ERROR: 1004 - искючение из таблицы.""",
                'id': 43
                }


class Number1005Error(RuCaptchaError):
    @staticmethod
    def answer():
        return {'text': """Блокировка на 5 минут.
                            Вы делаете слишком много запросов к res.php для получения ответов.
                        
                            При блокировке аккаунта используется следующее правило: R > C * 20 + 1200
                            Где:
                            R - число ваших запросов
                            C - число капч, которые вы загрузили
                            Это означает, что вы не должны обращаться к res.php за ответом для каждой капчи более 20 раз.
                            Пожалуйста, помните, что запрос баланса к res.php также учитывается!
                            Чтобы получать ваши ответы быстрее, без риска быть заблокированным,
                                вы можете использовать метод pingback и мы отправим вам ответ, как только решим вашу капчу.
                        
                            ERROR: 1005 - искючение из таблицы.""",
                'id': 44
                }
