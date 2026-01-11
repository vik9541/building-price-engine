# 📊 API Документация

## Базовые Информация

- **Base URL**: http://localhost:8000/api
- **Swagger UI**: http://localhost:8000/docs
- **Format**: JSON
- **Content-Type**: application/json

## Аутентификация

```bash
# Все админ эндпоинты требуют авторизацию
# (в настоящем выпуске она отключена для драфта)
```

## Навигация

1. [Products](#products) - Обработка товаров
2. [Competitors](#competitors) - Обработка конкурентов
3. [Prices](#prices) - Обработка цен
4. [Admin](#admin) - Админ операции

## Products

### Получить все товары

```
GET /api/products
```

**Параметры:**
- `skip` (integer, optional): Началющая позиция (default: 0)
- `limit` (integer, optional): Макс. кол-во на страницу (default: 100)
- `category` (string, optional): Фильтр по категории
- `is_active` (boolean, optional): Фильтр по активности

**Ответ:**
```json
[
  {
    "id": 1,
    "sku": "KIR001",
    "name": "Кирпич облицовочный",
    "category": "Кирпич и блоки",
    "cost": 15.0,
    "our_price": 25.0,
    "min_price": 22.0,
    "max_price": 28.0,
    "avg_competitor_price": 24.5,
    "is_active": true,
    "last_synced": "2026-01-11T10:00:00",
    "created_at": "2026-01-10T12:00:00",
    "updated_at": "2026-01-11T10:00:00"
  }
]
```

### Получить одно товаро

```
GET /api/products/{product_id}
```

**Ответ:**
```json
{
  "id": 1,
  "sku": "KIR001",
  "name": "Кирпич облицовочный",
  "description": "Красный марка 250×120×65",
  "category": "Кирпич и блоки",
  "cost": 15.0,
  "our_price": 25.0,
  "min_price": 22.0,
  "max_price": 28.0,
  "avg_competitor_price": 24.5,
  "main_image_url": "https://...",
  "is_active": true,
  "created_at": "2026-01-10T12:00:00",
  "updated_at": "2026-01-11T10:00:00"
}
```

### Создать товар

```
POST /api/products
```

**Отправка:**
```json
{
  "sku": "KIR001",
  "name": "Кирпич облицовочный",
  "description": "Красный марка 250×120×65",
  "category": "Кирпич и блоки",
  "cost": 15.0,
  "our_price": 25.0
}
```

### Обновить товар

```
PUT /api/products/{product_id}
```

**Отправка:**
```json
{
  "our_price": 26.0,
  "is_active": true
}
```

### Удалить товар

```
DELETE /api/products/{product_id}
```

## Competitors

### Получить всех конкурентов

```
GET /api/competitors
```

**Ответ:**
```json
[
  {
    "id": 1,
    "name": "Петрович",
    "competitor_type": "petrov",
    "base_url": "https://www.petrov.ru",
    "is_active": true,
    "last_parsed": "2026-01-11T10:00:00",
    "parse_status": "success",
    "parse_error": null
  }
]
```

## Prices

### Получить цены от конкурентов

```
GET /api/prices/{product_id}
```

**Ответ:**
```json
[
  {
    "id": 1,
    "product_id": 1,
    "competitor_id": 1,
    "price": 24.0,
    "old_price": null,
    "in_stock": true,
    "created_at": "2026-01-11T10:00:00"
  }
]
```

### Сравнить цены

```
GET /api/prices/compare/{product_id}
```

**Ответ:**
```json
{
  "product_id": 1,
  "product_name": "Кирпич облицовочный",
  "our_price": 25.0,
  "competitor_prices": [
    {
      "competitor": "Петрович",
      "price": 24.0,
      "url": "https://...",
      "in_stock": true
    }
  ]
}
```

## Admin

### Запустить парсинг

```
POST /api/admin/parse/petrov
```

**Ответ:**
```json
{
  "task_id": "abc123def456",
  "status": "queued"
}
```

### Получить статус парсинга

```
GET /api/admin/parse/status
```

**Ответ:**
```json
{
  "petrov": {
    "status": "success",
    "products_processed": 1500,
    "products_added": 50,
    "products_updated": 200,
    "duration_seconds": 45.3,
    "created_at": "2026-01-11T10:00:00"
  },
  "leroy_merlin": null,
  "obi": null
}
```
