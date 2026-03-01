# Curs

Демо-магазин электроники на Flask с каталогом товаров, корзиной, избранным, профилем пользователя и поиском с простыми NLP-эвристиками.

## Возможности

- каталог товаров с фильтрацией по категории, цене и сортировкой
- карточка товара с характеристиками
- регистрация, вход и профиль пользователя
- избранное и оформление заказа
- чат-помощник и API-поиск по каталогу
- PostgreSQL с начальными данными из `db/init.sql`

## Стек

- Python 3.11
- Flask
- SQLAlchemy / Flask-SQLAlchemy
- PostgreSQL 15
- Docker / Docker Compose
- `fuzzywuzzy` и `python-Levenshtein` для нечеткого поиска

## Структура проекта

```text
.
├── app.py
├── db/
│   └── init.sql
├── static/
├── templates/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Переменные окружения

Создайте `.env` в корне проекта:

```env
DB_NAME=shop
DB_USER=shop_user
DB_PASSWORD=shop_password
DB_HOST=db
DB_PORT=5432
```

## Запуск через Docker Compose

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

[http://localhost:5002](http://localhost:5002)

## Локальный запуск без Docker

1. Создайте виртуальное окружение и установите зависимости:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Поднимите PostgreSQL и создайте базу с данными из `db/init.sql`.

3. Укажите переменные окружения и запустите приложение:

```bash
python app.py
```

Приложение слушает порт `5000`.

## Основные маршруты

- `/` - главная страница
- `/catalog` - каталог товаров
- `/product/<id>` - карточка товара
- `/cart` - корзина
- `/checkout` - оформление заказа
- `/profile` - профиль пользователя
- `/chat` - чат-помощник
- `/api/search_catalog` - API-поиск

## Примечания

- `.env` исключен из git и не публикуется в репозитории
- `app.secret_key` в `app.py` сейчас демонстрационный и для production должен быть заменен
- приложение запускается в `debug=True`, что подходит только для локальной разработки
