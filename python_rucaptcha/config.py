# ключ приложения
app_key = "1899"


# генератор в котором задаётся кол-во попыток на повторное подключение
def connect_generator():
    for i in range(5):
        yield i
