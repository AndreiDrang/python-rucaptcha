import sqlite3
import json

class Database:
    def __init__(self):
        self.db_connect = sqlite3.connect('python_rucaptcha.db')
        self.db_cursor = self.db_connect.cursor()

    # Создаём таблицы для работы
    def creating_tables(self):
        # Добавляем таблицу с прокси
        self.db_cursor.execute('''
					CREATE TABLE IF NOT EXISTS common_captcha(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    captcha_img_source TEXT,
                    captcha_key TEXT);''')

        # Добавляем таблицу в которой будет сохранены данные аккаунтов
        self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS text_captcha(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    captcha_text TEXT,
                    captcha_key TEXT);''')

        # Вносим изменения
        self.db_connect.commit()

    # Закрываем соединение с БД
    def __del__(self):
        self.db_connect.close()
        