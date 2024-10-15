# MovieParser

1. Склонируйте репозиторий:
```
git clone https://github.com/boif/MParser.git
cd MParser
```

2. Создайте виртуальное окружение:
```
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate  # Для Windows
```
3. Установите зависимости:
```
pip install -r requirements.txt
```
4. Настройте базу данных. Обновите переменные окружения в вашем файле .env:
```
# Настройки базы данных для вашего проекта.

DB_NAME=movies
DB_USER=ваш_пользователь
DB_PASSWORD=ваш_пароль
DB_HOST=db
DB_PORT=5432

POSTGRES_DB=movies
POSTGRES_USER=ваш_пользователь
POSTGRES_PASSWORD=ваш_пароль
DATABASE_URL=postgres://ваш_пользователь:ваш_пароль@db:5432/movies
```
5. Запустите контейнеры с помощью Docker Compose:
```
docker-compose up --build / docker compose up --build
```

![photo_2024-10-15_00-28-01](https://github.com/user-attachments/assets/4f1e534a-655c-4d35-8cda-c5b31d829348)
![photo_2024-10-15_00-28-46](https://github.com/user-attachments/assets/7faf8cd7-78ae-40a7-a7bd-72e01edb2a41)
