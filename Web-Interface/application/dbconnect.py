import sqlite3
import json

class Database:
    def __init__(self):
        self.db_connect = sqlite3.connect('python_rucaptcha.db')
        self.db_cursor = self.db_connect.cursor()

    # Создаём таблицы для работы
    def creating_tables(self):
        # Добавляем таблицу c текстовой капчёй
        self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS text_captcha(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    captcha_text TEXT UNIQUE ,
                    captcha_key TEXT);''')

        # Вносим изменения
        self.db_connect.commit()
    
    # Получение списка вопросов и ответов тектсовой капчи
    def get_text_captcha(self):
        self.db_cursor.execute('''SELECT captcha_text, captcha_key FROM text_captcha''')
        
        return self.db_cursor.fetchall()


    # Закрываем соединение с БД
    def __del__(self):
        self.db_connect.close()

        