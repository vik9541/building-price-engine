# 🚀 Установка и Настройка

## Предположения

- Docker & Docker Compose
- Git
- Python 3.11+ (для локальной разработки)

## Шаг 1: Клонирувание Проекта

```bash
git clone https://github.com/vik9541/building-price-engine.git
cd building-price-engine
```

## Шаг 2: Настройка Окружения

```bash
# Настройка environment variables
cp backend/.env.example backend/.env

# Отредактируйте backend/.env если нужно
```

## Шаг 3: Монтирование Всех Сервисов

```bash
# Построить и запустить
docker-compose up -d

# Проверить статус
docker-compose ps
```

## Шаг 4: Инициализация БД

```bash
# Выполнить миграции
docker-compose exec backend python -m alembic upgrade head

# Но пока alembic не конфигурируются, 
# база сохдастя автоматически при запуске backend
```

## Шаг 5: Проверка Доступа

Опените в браузере:

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432 (user: user, password: password)
- **Redis**: localhost:6379

## Основные Команды

```bash
# Посмотреть логи
docker-compose logs -f backend
docker-compose logs -f celery

# Остановить все сервисы
docker-compose down

# Очистить все данные
docker-compose down -v

# Перестартовать конкретные сервисы
docker-compose restart backend
docker-compose restart celery
```

## Локальная Разработка

### Настройка Виртуального Окружения

```bash
cd backend
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### Запуск апи

```bash
cd backend
uvicorn app.main:app --reload
```

### Локальные Унит-тесты

```bash
pytest
pytest -v
pytest --cov=app
```

## Продакшн Продеплой

```bash
# Ског docker-compose.yml для production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
