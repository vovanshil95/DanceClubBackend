# Серверная часть приложения для студии танцев
Проект выполнен в рамках учебной проектной деятельности в Университете ИТМО. 
Приложение решает реальную проблему, связанную с неудобством пользователя записываться на секции, смотреть расписание и количество свободных мест. Все данные предоставляются сервером, но в том числе хранятся локально (после первой авторизации), так что при отсутствии изменений в расписании оно будет доступлно оффлайн.
На данный момент проект находится в процессе разработки.

## Клиент и Сервер
Данный репозиторий является backend-частью разрабатываемого приложения.
Репозиторий с клиентом находится [здесь](https://github.com/vladryanka/DanceClub).

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Deploy и CI/CD](#deploy-и-cicd)
- [Команда проекта](#команда-проекта)

## Технологии
- Python 3.11
- PostgreSQL (psql) - основная СУБД
- Docker
- Unicorn (FastAPI)
- Alembic
- asyncio 

## Использование

### Документация
[Документация](http://195.54.178.243:25433/docs) по проекту сделана с помощью Swagger.

### Запуск
Для запуска сервера необходимо выполнить следующие шаги:

Установка зависимостей сервера
```shell
apt-get update && apt-get install -y nohup
sudo apt install python3-venv
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
```

Запуск Docker-контейнера с PostgreSQL
```shell
sudo docker run -d \
  --name dance-club-db \
  -e POSTGRES_DB=dance_club_db \
  -e POSTGRES_USER=dance_club_user \
  -e POSTGRES_PASSWORD={ваш пароль от бд} \
  -p 5432:5432 \
  postgres
```

Создание файла .env
```shell
echo "DB_NAME=dance_club_db" >> .env
echo "DB_USER=dance_club_user" >> .env
echo "DB_PASS={ваш пароль от бд}" >> .env
echo "DB_PORT=5432" >> .env
echo "DB_HOST=localhost" >> .env
echo "ORIGINS={ip вашего frontend сервера}" >> .env
```

Создание и активация виртуального окружения
```shell
python -m venv venv
source venv/bin/activate
```

Установка зависимостей pip
```shell
pip install -r requirements.txt
```

Обновление сущностей в бд
```shell
alembic upgrade head
```

Запуск приложения
```shell
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > output.log 2>&1 &
```

### Разработка
Необходимые для работы проекта библиотеки и их версии перечислены в [файле версий](/requirements.txt).
Основное:
- Python 3.11
- PostgreSQL (psql)
- Docker
- FastAPI

## Deploy и CI/CD
..

## Команда проекта
- Android
  - @trombbone - Team Lead & Android-developer
  - @vladryanka - Android-developer
- Server (Python)
  - @vovanshil95 - Backend-developer
  - @P0linaria - Documentarian & Backend-developer
