# Codeforces parser

### Как запустить проект:

В папке infra создайте и заполните .env файл:
```
TOKEN=(Токен телеграм бота)

DB_NAME=(Имя базы данных)
POSTGRES_USER=(Имя юзера)
POSTGRES_PASSWORD=(Пароль)
DB_HOST=db
DB_PORT=5432
```
Из папки infra выполните:
```
docker-compose up --build
```

### Автор
Данил Воронин https://github.com/Bogdan-Malina
