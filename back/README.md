### 1. Create virtual environment

```shell
python -m venv venv
```

### 2. Activate virtual environment

```shell
source venv/bin/activate
```

### 3. Install requirements

```shell
pip install -r requirements.txt
```

### 4. Create .env file from .env.example

- SECRET_KEY - секретный ключ
- ALLOWED_HOSTS - список строк, представляющих имена хостов/доменов, которые может обслуживать сайт
- CORS_ALLOWED_ORIGINS - список источников, которым разрешено выполнять межсайтовые HTTP-запросы
- DEBUG - режим отладки
- POSTGRES_DB - название базы данных
- POSTGRES_USER - пользователь
- POSTGRES_PASSWORD - пароль
- POSTGRES_HOST - хост
- POSTGRES_PORT - порт

### 5. Apply migrations

```shell
python manage.py migrate
```

### 6. Create super user

```shell
python manage.py createsuperuser
```

### 7. Run server

```shell
python manage.py runserver
```
