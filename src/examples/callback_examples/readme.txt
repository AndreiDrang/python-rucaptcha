1. Установка на сервере: aiohttp, aio_pika, pymemcache, rebbitmq-server, memcached.
   Установка на клиенте: aiohttp, pika.
2. Открытие портов на сервере:
    - порт для работы callback-server'a;
    - порты для подключения к rabbitmq - 5672 и 15672(при желании)
3. Установка плагинов для rabbitmq-статистики.
4. Создание виртуального хоста(или нескольких, для каждого сервиса).
5. Создание пользователя с ограниченными правами(только чтение) доступа к определённому хосту.
rabbitmqctl set_permissions -p <VHOST> <USERNAME> "^$" "^$" ".*"
6. Создание аккаунта с правами на запись/изменение данных хоста.
rabbitmqctl set_permissions -p <VHOST> <USERNAME> ".*" ".*" "^$"
7. Запуск callback-server'a.