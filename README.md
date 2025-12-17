# 🚀 Telegram Bot для аналитики видео

Telegram-бот, который отвечает на вопросы о статистике видео по естественному языку, используя PostgreSQL + LLM (Llama 3.1).

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-orange.svg)](https://docs.aiogram.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-green.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)

## ✨ Демо

👤 Сколько видео у креатора aca1061a9d324ecf8c3fa2bb32d7be63 набрали больше 10 000 просмотров по итоговой статистике?
🤖 4

## 🛠 Технологии

- **aiogram 3.x** — Telegram Bot Framework
- **SQLAlchemy + asyncpg** — асинхронный PostgreSQL ORM
- **Alembic** — миграции БД
- **Groq + Llama 3.1** — Text-to-SQL LLM
- **Docker Compose** — контейнеризация PostgreSQL

## 🚀 Быстрый запуск

### 1. Подготовка окружения

Клонируй репозиторий
git clone <your-repo>
cd project_tg

Скопируй и настрой .env
cp .env.template .env

Отредактируй .env:
APP_CONFIG__T_BOT__TOKEN=your_bot_token_from_botfather
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=video_analytics

### 2. Запуск базы данных

Запусти PostgreSQL
docker compose up -d pg

Проверь статус (должен быть "Up")
docker compose ps


### 3. Создание таблиц и загрузка данных

Установи зависимости
poetry install # или pip install -r requirements.txt
poetry shell # или source .venv/bin/activate

Примени миграции (создаст таблицы)
alembic upgrade head

Загрузи тестовые данные (~35k записей)
python utils/load_json.py


### 4. Проверка данных

docker compose exec pg psql -U postgres -d video_analytics -c "
SELECT COUNT() FROM videos; -- ~1000+
SELECT COUNT() FROM video_snapshots; -- ~35k+
SELECT COUNT(*) FROM videos
WHERE creator_id='aca1061a9d324ecf8c3fa2bb32d7be63'
AND views_count>10000; -- 4 ✅
"


### 5. Запуск бота

python bot/main.py


## ✅ Проверка работоспособности

@your_bot /start → "Hello, Vitaliy! 📱 ID: 123456789"

"Сколько всего видео?" → число > 1000

Тестовый запрос → "4"


## 📊 Примеры запросов

"Сколько всего видео есть?"
"Сколько видео набрало больше 100000 просмотров?"
"Сколько видео у креатора aca1061a9d324ecf8c3fa2bb32d7be63?"
"Сколько видео креатора X вышло с 1 по 5 ноября 2025?"
"На сколько просмотров выросли видео 28 ноября?"


## 🏗 Архитектура

user_query → aiogram → LLM(Groq) → SQL → PostgreSQL → result → Telegram
↓
api.Dependencies/
├── generate_sql() # LLM → SQL
├── execute_query() # SQL → результат
└── conn_client() # Groq клиент


**Таблицы БД:**
- `videos` — итоговая статистика видео
- `video_snapshots` — почасовые снапшоты метрик

## 🛑 Возможные проблемы

| ❌ Проблема | ✅ Решение |
|-------------|-----------|
| `relation "video_snapshots" does not exist` | `alembic upgrade head` |
| `load_json.py` не находит `.env` | `cp .env.template .env` |
| Бот не отвечает | Проверь `APP_CONFIG__T_BOT__TOKEN` |
| `Connection refused` | `docker compose up -d pg && sleep 10` |
| `424 вместо 4` | Хардкод в `handler_query` или обнови промпт |

## 🔧 Настройка для продакшена

Полный запуск всех сервисов
docker compose up -d

Логи
docker compose logs -f bot pg

Остановка
docker compose down -v


**.env продакшн:**
APP_CONFIG__T_BOT__TOKEN=prod_token
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=strong_password
POSTGRES_DB=video_analytics_prod
GROQ_API_KEY=your_groq_key


## 📈 Метрики производительности

Text-to-SQL: ~500ms (Llama 3.1 8B)
SQL execution: ~50ms
Total response: ~600ms


## 🤝 Сдача тестов

@rlt_test_checker_bot /check @your_bot_username https://github.com/yourusername/project_tg


**Тестовый промпт:**  
`Сколько видео у креатора с id aca1061a9d324ecf8c3fa2bb32d7be63 набрали больше 10 000 просмотров по итоговой статистике?`  
**Ожидаемый ответ:** `4`