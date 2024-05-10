# Telegram бот для управления подписками и автопостинга

Бот предназначен для управления подписками пользователей на канал и автоматического постинга сообщений в групповой чат.

## Функции бота

### Подписка на канал

Бот проверяет, подписан ли пользователь на канал. Если пользователь подписан, он может свободно писать сообщения в групповом чате. Если пользователь не подписан на канал, его сообщения в чате удаляются, и ему отправляется предупреждение. После 5 предупреждений пользователь удаляется из чата.

### Автопостинг

Бот также имеет функцию автопостинга. Пользователь может установить время и дату для поста, отправив сообщение боту в режиме диалога. Бот автоматически отправит сообщение в групповой чат в указанное время и дату.

## Установка и запуск


### Установка зависимостей:

Установите необходимые зависимости, указанные в файле requirements.txt, выполнив следующую команду:
 ```bash
pip install -r requirements.txt
```
### Создание базы данных PostgreSQL:
Создайте базу данных PostgreSQL для бота. Вы можете использовать команду createdb, как указано ниже:
```bash
sudo -u postgres createdb moderator
```
### Создание файла .env:
Создайте файл .env в корневой папке проекта и добавьте в него переменные окружения BOT_TOKEN и DATABASE_CONNECTION_URL, как показано ниже:
```plantext
BOT_TOKEN=<токен_бота>
DATABASE_CONNECTION_URL=postgres://postgres:<пароль>@localhost:5432/moderator
```
Замените пароль на ваш пароль для доступа к PostgreSQL.

### Запуск бота:
Запустите основной скрипт бота, выполнив следующую команду:
 ```bash
python main.py
```

### Команды
addchannel - добавляет канал 

select_chat - выбор чата для контроля
