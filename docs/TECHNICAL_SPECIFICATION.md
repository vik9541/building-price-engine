# 🏗️ ТЕХНИЧЕСКОЕ ЗАДАНИЕ (ТЗ)
# Building Materials Price Engine & Catalog System

**Версия:** 1.0  
**Дата:** 11.01.2026  
**Статус:** В разработке

---

## 📋 ОГЛАВЛЕНИЕ

1. [Цель проекта](#цель-проекта)
2. [Описание функционала](#описание-функционала)
3. [Архитектура системы](#архитектура-системы)
4. [Требования к БД](#требования-к-бд)
5. [Парсеры и источники данных](#парсеры-и-источники-данных)
6. [Ценообразование](#ценообразование)
7. [API](#api)
8. [Планы развития](#планы-развития)
9. [Сроки и ресурсы](#сроки-и-ресурсы)

---

## 🎯 ЦЕЛЬ ПРОЕКТА

### Основная задача
Создать **автоматизированную систему управления каталогом строительных материалов и оборудования** с:
- Полной номенклатурой всех строительных товаров
- Мониторингом цен у минимум **100+ поставщиков на каждый товар**
- Аналитикой рынка (цены закупки, розницы, тренды)
- Автоматическим формированием цен на основе конкурентного анализа

### Целевая аудитория
- **B2B**: Закупщики строительных компаний
- **B2C**: Розничные покупатели через сайт
- **Внутренний**: Логистика, закупки, маркетинг

### Бизнес-метрика
Уменьшить затраты на строматериалы на **15-25%** через оптимальную закупку и конкурентное ценообразование.

---

## 📦 ОПИСАНИЕ ФУНКЦИОНАЛА

### 1️⃣ КАТАЛОГ ТОВАРОВ

#### 1.1 Полнота номенклатуры

**Источники данных:**
```
Примарные источники (обязательны):
├─ Петровичи (petrov.ru)           ✅ Главный источник
├─ Leroy Merlin (leroymerlin.ru)    ✅ Крупный игрок
├─ OBI (obi.ru)                      ✅ Крупный игрок
├─ Avangard (avangard.ru)            ✅ Региональный
└─ E-Catalog (e-catalog.ru)          ✅ Агрегатор

Вторичные источники (желательны):
├─ Stroydom.ru
├─ Yarmarkt.ru
├─ MasterOK.ru
├─ Stroyplet.ru
└─ Regionalnye-magaziny.ru (3-5 региональных)
```

**Категории товаров:**
```
1. КРОВЕЛЬНЫЕ МАТЕРИАЛЫ
   ├─ Металлочерепица
   ├─ Профнастил
   ├─ Гибкая черепица
   ├─ Ондулин
   └─ Комплектующие (коньки, ендовы, флешинги)

2. КИРПИЧ И БЛОКИ
   ├─ Кирпич облицовочный
   ├─ Кирпич рядовой
   ├─ Газобетонные блоки
   ├─ Пенобетонные блоки
   ├─ Керамические блоки
   └─ Фундаментные блоки

3. ОТДЕЛОЧНЫЕ МАТЕРИАЛЫ
   ├─ Краски (акриловые, масляные, водоэмульсионные)
   ├─ Обои (флизелиновые, виниловые, бумажные)
   ├─ Плитка керамическая
   ├─ Керамогранит
   ├─ Панели ПВХ
   ├─ МДФ панели
   └─ Паркет и ламинат

4. ИЗОЛЯЦИОННЫЕ МАТЕРИАЛЫ
   ├─ Минеральная вата
   ├─ Пенополистирол (ПСБ, ХПС)
   ├─ Пенополиуретан
   ├─ Пробковые материалы
   └─ Фольга и пароизоляция

5. ГИПСОКАРТОН И ШПАКЛЁВКА
   ├─ ГКЛ стандартный
   ├─ ГКЛ влагостойкий
   ├─ ГКЛ огнестойкий
   ├─ Профили (ПН, ПС)
   ├─ Шпаклёвка (гипсовая, полимерная)
   └─ Грунтовки

6. САНТЕХНИКА И ТРУБОПРОВОДЫ
   ├─ Трубы (металлические, пластиковые)
   ├─ Фитинги
   ├─ Батареи отопления
   ├─ Смесители
   └─ Сантехническая арматура

7. ЭЛЕКТРИКА
   ├─ Кабели и провода
   ├─ Выключатели и розетки
   ├─ Распределительные щиты
   ├─ Автоматические выключатели
   └─ УЗО и дифавтоматы

8. ИНСТРУМЕНТ
   ├─ Ручной инструмент
   ├─ Электроинструмент
   ├─ Измерительный инструмент
   └─ Спецодежда и СИЗ

9. КРЕПЁЖ И РАСХОДНИКИ
   ├─ Саморезы
   ├─ Гвозди
   ├─ Анкеры
   ├─ Дюбеля
   ├─ Клей и герметики
   ├─ Монтажная пена
   └─ Лента и скотч

10. ДВЕРИ И ОКНА
    ├─ Входные двери
    ├─ Межкомнатные двери
    ├─ Пластиковые окна
    ├─ Деревянные окна
    └─ Комплектующие (петли, ручки, уплотнители)

11. НАПОЛЬНЫЕ ПОКРЫТИЯ
    ├─ Ламинат
    ├─ Паркет
    ├─ Линолеум
    ├─ ПВХ плитка (LVT)
    └─ Пробковое покрытие

12. КРОВЕЛЬНЫЕ КОМПЛЕКТУЮЩИЕ
    ├─ Коньки
    ├─ Ендовы
    ├─ Флешинги
    ├─ Система водостока
    └─ Подкладочный ковер

13. ПРОЧИЕ МАТЕРИАЛЫ
    ├─ Цемент и песок
    ├─ Бетон и растворы
    ├─ Геотекстиль
    ├─ Мембраны кровельные
    └─ Тепловизионная краска
```

**Целевой объём каталога:**
- **Минимум**: 15,000 артикулов
- **Оптимум**: 50,000 артикулов
- **Максимум**: 100,000+ артикулов

#### 1.2 Структура товара в БД

```python
PRODUCT = {
    # Идентификация
    "id": int,                           # Уникальный ID в системе
    "sku": str,                          # Артикул (уникальный)
    "barcode": str,                      # Штрихкод (если есть)
    
    # Базовая информация
    "name": str,                         # Название
    "description": str,                  # Полное описание
    "category": str,                     # Категория (из структуры выше)
    "subcategory": str,                  # Подкатегория
    "brand": str,                        # Производитель
    "model": str,                        # Модель
    
    # Физические параметры
    "dimensions": {
        "length": float,                 # Длина (см)
        "width": float,                  # Ширина (см)
        "height": float,                 # Высота (см)
        "weight": float,                 # Вес (кг)
        "unit": str,                     # Единица (шт, м², м³, л, кг и т.д.)
        "quantity_per_unit": int,        # Кол-во в упаковке
    },
    
    # Характеристики
    "specifications": {
        "color": str,
        "material": str,
        "quality_grade": str,            # Класс, марка
        "fire_rating": str,              # Огнестойкость
        "water_resistance": str,         # Влагостойкость
        "durability_years": int,         # Срок службы
        "custom_specs": dict,            # Специфичные для категории
    },
    
    # Изображения
    "images": [
        {
            "url": str,                  # URL фото
            "source": str,               # Откуда взяли
            "type": str,                 # main, gallery, size_chart
            "cached_local_path": str,    # Локальное хранилище
        }
    ],
    
    # Наша цена (расчётная)
    "our_price": float,                  # Текущая цена
    "cost_price": float,                 # Себестоимость (средняя)
    "markup_percent": float,             # Наценка %
    "margin_rub": float,                 # Маржа в рублях
    
    # Статусы
    "is_active": bool,                   # Активен ли товар
    "is_bestseller": bool,               # Хит продаж
    "stock_status": str,                 # in_stock, pre_order, out_of_stock
    
    # Сроки и доставка
    "delivery_days": int,                # Среднее время доставки
    "shipping_weight": float,            # Вес для расчёта доставки
    
    # Метаданные
    "created_at": datetime,              # Дата создания
    "updated_at": datetime,              # Дата обновления
    "last_synced": datetime,             # Последняя синхронизация
}
```

### 2️⃣ ИСТОЧНИКИ ЦЕН И КОНКУРЕНТЫ

#### 2.1 Поставщики (где закупать)

**Требование: минимум 100+ источников ЦЕН на каждый товар**

```
ТИПЫ ИСТОЧНИКОВ:

1. ОНЛАЙН МАГАЗИНЫ (основной источник)
   ├─ Крупные маркетплейсы (Яндекс.Маркет, 1С-Битрикс)
   ├─ Специализированные сайты
   ├─ Интернет-магазины производителей
   ├─ Региональные интернет-магазины
   └─ Агрегаторы цен

2. B2B ПЛАТФОРМЫ (оптовые цены)
   ├─ Alibaba / AliExpress
   ├─ Global Sources
   ├─ Made-in-China
   ├─ Российские B2B (Алибаба.рф, Индустриалпро)
   └─ Специализированные B2B порталы

3. РОЗНИЧНЫЕ СЕТИ (для ориентира)
   ├─ Петрович (обязательно)
   ├─ Leroy Merlin (обязательно)
   ├─ OBI (обязательно)
   ├─ Avangard (обязательно)
   └─ Региональные сети

4. ПРОИЗВОДИТЕЛИ
   ├─ Прямые цены производителей
   ├─ Официальные дистрибьюторы
   └─ Представительства в регионах

5. АУКЦИОНЫ И ТОРГИ
   ├─ 44-ФЗ закупки
   ├─ 223-ФЗ закупки
   ├─ Аукционы электроэнергии
   └─ Специализированные аукционы
```

#### 2.2 Источники данных (где берём цены)

```python
PRICE_SOURCE = {
    "id": int,
    "name": str,                    # Название источника
    "source_type": str,             # retailer, wholesaler, marketplace, manufacturer, aggregator
    "base_url": str,                # URL сайта
    "api_available": bool,          # Есть ли API
    "api_endpoint": str,            # Эндпоинт API
    "parse_method": str,            # html_parsing, api, csv_export, manual
    
    # Параметры парсинга
    "check_interval_minutes": int,  # Как часто проверяем (60, 120, 240)
    "reliability_score": float,     # Надёжность 0-100
    "response_time_ms": int,        # Время ответа
    "success_rate_percent": float,  # Процент успешных парсинговых сессий
    
    # Статистика
    "total_products_tracked": int,  # Сколько товаров отслеживаем
    "price_updates_total": int,     # Всего обновлений
    "last_checked": datetime,       # Когда последний раз проверили
    "last_error": str,              # Последняя ошибка
    
    "is_active": bool,
    "weight_in_calculations": float, # Вес при расчёте (0.0-1.0)
}
```

---

## 🏛️ АРХИТЕКТУРА СИСТЕМЫ

### 3.1 Общая схема

```
┌─────────────────────────────────────────────────────────────┐
│                       FRONTEND / API                         │
│  (Каталог для B2C, API для интеграций)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    BACKEND (FastAPI)                        │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │
│  │ Price  │ │Catalog │ │Monitor │ │ Admin  │ │ Pricing│  │
│  │ Manage │ │ Manage │ │        │ │ Panel  │ │ Engine │  │
│  └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘  │
└──────┼──────────┼──────────┼──────────┼──────────┼────────┘
       │          │          │          │          │
       └──────────┴──────────┴──────────┴──────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    WORKERS (Celery)                         │
│  ┌─────────────┐ ┌──────────────┐ ┌─────────────┐        │
│  │   Parsers   │ │   Monitoring │ │   Pricing   │        │
│  │ (100+ sites)│ │   (24/7)     │ │ (calc. &    │        │
│  │             │ │              │ │  update)    │        │
│  └─────────────┘ └──────────────┘ └─────────────┘        │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  DATABASE (PostgreSQL)                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ Products │ │  Prices  │ │ Analysis │ │ History  │     │
│  │          │ │          │ │          │ │          │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  CACHE (Redis)                              │
│  - Кэш цен для быстрого доступа                             │
│  - Очередь задач Celery                                     │
│  - Сессии пользователей                                     │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 Процесс сбора данных

```
┌─ ПАРСИНГ КОНКУРЕНТОВ (каждый час) ─┐
│                                      │
├─ Подключение к 100+ источникам       │
├─ Извлечение товаров и цен           │
├─ Матчинг (связь товаров)            │
├─ Валидация данных                    │
└──────────┬──────────────────────────┘
           │
           ▼
┌─ СОХРАНЕНИЕ В БД ──┐
│                    │
├─ CompetitorPrice   │
├─ PriceSnapshot     │
├─ ProductMapping    │
└────────┬───────────┘
         │
         ▼
┌─ АНАЛИЗ РЫНКА ─────┐
│                    │
├─ Статистика цен    │
├─ Тренды            │
├─ Позиция          │
├─ Аномалии         │
└────────┬───────────┘
         │
         ▼
┌─ ПЕРЕСЧЁТ НАШИХ ЦЕН ─┐
│                       │
├─ Стратегия           │
├─ Конкурентная цена   │
├─ Маржа               │
└───────────┬───────────┘
            │
            ▼
┌─ ОБНОВЛЕНИЕ КАТАЛОГА ─┐
│                       │
├─ Our_price           │
├─ Recommended_price   │
├─ Price_history       │
└───────────────────────┘
```

---

## 🗄️ ТРЕБОВАНИЯ К БД

### 4.1 Основные таблицы

```sql
-- ТОВАРЫ
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(500) NOT NULL,
    description TEXT,
    category VARCHAR(200),
    subcategory VARCHAR(200),
    brand VARCHAR(200),
    
    -- Физ. параметры
    length FLOAT,
    width FLOAT,
    height FLOAT,
    weight FLOAT,
    unit VARCHAR(50),
    quantity_per_unit INT,
    
    -- Наша цена
    our_price FLOAT,
    cost_price FLOAT,
    markup_percent FLOAT,
    
    -- Статус
    is_active BOOLEAN DEFAULT true,
    stock_status VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_synced TIMESTAMP,
    
    INDEX idx_sku (sku),
    INDEX idx_category (category),
    INDEX idx_brand (brand)
);

-- ИСТОЧНИКИ ЦЕН
CREATE TABLE price_sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL,
    source_type VARCHAR(50),
    base_url VARCHAR(500),
    api_available BOOLEAN,
    check_interval_minutes INT DEFAULT 60,
    reliability_score FLOAT DEFAULT 100,
    
    total_products_tracked INT DEFAULT 0,
    last_checked TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ЦЕНЫ КОНКУРЕНТОВ (текущие)
CREATE TABLE competitor_prices (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    source_id INT REFERENCES price_sources(id),
    
    competitor_sku VARCHAR(200),
    competitor_url VARCHAR(1000),
    price FLOAT NOT NULL,
    old_price FLOAT,
    
    in_stock BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_product_source (product_id, source_id),
    INDEX idx_price (price)
);

-- СНИМКИ ЦЕН (история)
CREATE TABLE price_snapshots (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    source_id INT REFERENCES price_sources(id),
    price FLOAT NOT NULL,
    in_stock BOOLEAN,
    
    market_position VARCHAR(50),
    deviation_from_avg FLOAT,
    
    snapshot_date TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_product_date (product_id, snapshot_date),
    INDEX idx_source_date (source_id, snapshot_date)
);

-- АНАЛИЗ РЫНКА
CREATE TABLE market_analysis (
    id SERIAL PRIMARY KEY,
    product_id INT UNIQUE REFERENCES products(id),
    
    active_sellers_count INT,
    price_min FLOAT,
    price_max FLOAT,
    price_avg FLOAT,
    price_median FLOAT,
    price_std_dev FLOAT,
    
    our_position VARCHAR(50),
    our_price_percentile FLOAT,
    
    yandex_market_price FLOAT,
    yandex_market_deviation FLOAT,
    
    price_trend VARCHAR(50),
    price_trend_24h FLOAT,
    price_trend_7d FLOAT,
    price_trend_30d FLOAT,
    
    analysis_date TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_product (product_id),
    INDEX idx_date (analysis_date)
);

-- РЕЙТИНГ ЦЕН
CREATE TABLE competitor_price_ranking (
    id SERIAL PRIMARY KEY,
    product_id INT UNIQUE REFERENCES products(id),
    
    total_competitors INT,
    our_rank INT,
    price_above_cheapest FLOAT,
    price_below_expensive FLOAT,
    
    recommended_price FLOAT,
    recommendation_reason TEXT,
    
    analysis_date TIMESTAMP DEFAULT NOW()
);

-- ОПОВЕЩЕНИЯ
CREATE TABLE price_alerts (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    source_id INT REFERENCES price_sources(id),
    
    alert_type VARCHAR(50),  -- price_drop, price_spike, outlier
    old_price FLOAT,
    new_price FLOAT,
    change_percent FLOAT,
    
    message TEXT,
    is_acknowledged BOOLEAN DEFAULT false,
    
    created_at TIMESTAMP DEFAULT NOW(),
    acknowledged_at TIMESTAMP,
    
    INDEX idx_product (product_id),
    INDEX idx_date (created_at)
);

-- ИСТОРИЯ ЦЕН
CREATE TABLE price_history (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    
    old_price FLOAT,
    new_price FLOAT,
    change_reason VARCHAR(200),
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_product_date (product_id, created_at)
);

-- СООТВЕТСТВИЯ ТОВАРОВ
CREATE TABLE product_source_mappings (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    source_id INT REFERENCES price_sources(id),
    
    source_product_id VARCHAR(200),
    source_product_url VARCHAR(1000),
    source_product_name VARCHAR(500),
    
    match_score FLOAT,  -- 0-100
    match_method VARCHAR(50),  -- sku_match, name_match, manual
    
    last_price FLOAT,
    last_price_update TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_product_source (product_id, source_id)
);
```

**Требования:**
- PostgreSQL 14+
- Размер БД: 500GB-1TB (при 100К товаров × 100 источников × 2 года истории)
- Репликация и backup ежедневно

---

## 🔍 ПАРСЕРЫ И ИСТОЧНИКИ ДАННЫХ

### 5.1 Обязательные источники (Tier 1)

```
┌─ ПЕТРОВИЧ ──────────────────────────────┐
│ URL: petrov.ru                          │
│ Товаров: ~30,000                        │
│ Интервал: 60 минут                      │
│ Метод: HTML parsing (BeautifulSoup)     │
│ Сложность: Средняя                      │
│ Статус: Готов к разработке             │
└─────────────────────────────────────────┘

┌─ LEROY MERLIN ──────────────────────────┐
│ URL: leroymerlin.ru                     │
│ Товаров: ~35,000                        │
│ Интервал: 60 минут                      │
│ Метод: API (if available) / JS rendering│
│ Сложность: Высокая (JS)                 │
│ Статус: Готов к разработке             │
└─────────────────────────────────────────┘

┌─ OBI ───────────────────────────────────┐
│ URL: obi.ru                             │
│ Товаров: ~25,000                        │
│ Интервал: 60 минут                      │
│ Метод: HTML parsing                     │
│ Сложность: Средняя                      │
│ Статус: Готов к разработке             │
└─────────────────────────────────────────┘

┌─ YANDEX MARKET ─────────────────────────┐
│ URL: market.yandex.ru                   │
│ Тип: Агрегатор (100+ магазинов)         │
│ Интервал: 120 минут                     │
│ Метод: API (с ключом)                   │
│ Сложность: Высокая (API)                │
│ Статус: В разработке                    │
└─────────────────────────────────────────┘
```

### 5.2 Дополнительные источники (Tier 2)

```
┌─ E-CATALOG ─────────────────────────────┐
│ URL: e-catalog.ru                       │
│ Тип: Агрегатор цен                      │
│ Товаров: 50,000+                        │
│ Интервал: 240 минут                     │
│ Метод: CSV export / API                 │
│ Статус: К разработке                    │
└─────────────────────────────────────────┘

┌─ AVANGARD ──────────────────────────────┐
│ URL: avangard.ru                        │
│ Тип: Региональная сеть                  │
│ Товаров: 10,000+                        │
│ Интервал: 180 минут                     │
│ Метод: HTML parsing                     │
│ Статус: К разработке                    │
└─────────────────────────────────────────┘

┌─ ALIBABA / ALIEXPRESS ──────────────────┐
│ URL: alibaba.com / aliexpress.com       │
│ Тип: B2B (оптовые поставки)             │
│ Товаров: Все категории                  │
│ Интервал: 480 минут (2 часа)            │
│ Метод: API (с ключом) / Parsing         │
│ Статус: К разработке                    │
└─────────────────────────────────────────┘

┌─ ПРОИЗВОДИТЕЛИ ─────────────────────────┐
│ Прямое взаимодействие                   │
│ Задача: Собрать 50+ производителей     │
│ Метод: API или CSV-export               │
│ Интервал: 480 минут (4 часа)            │
│ Статус: К разработке                    │
└─────────────────────────────────────────┘
```

### 5.3 Требования парсера

**На КАЖДЫЙ товар должны собраться:**
```
✅ Минимум 5 источников цен (обязательно)
✅ Минимум 20 источников ЦЕН (оптимально)
✅ 100+ источников ЦЕН (целевой показатель)

Для каждого источника:
├─ Текущая цена
├─ Старая цена (для скидок)
├─ Статус наличия
├─ Ссылка на товар
├─ Дата/время обновления
└─ Надёжность источника
```

---

## 💰 ЦЕНООБРАЗОВАНИЕ

### 6.1 Алгоритм расчёта цены

```python
def calculate_optimal_price(product):
    """
    Расчёт оптимальной цены продажи на основе анализа рынка
    """
    
    # 1. БАЗОВАЯ ЦЕНА (минимальная маржа)
    base_price = product.cost_price * (1 + MIN_MARKUP / 100)
    # Пример: cost=100р × 1.10 = 110р
    
    # 2. СБОР ДАННЫХ О КОНКУРЕНТАХ
    competitor_prices = get_competitor_prices(product)
    # Петрович: 125р, Leroy: 130р, OBI: 120р, ...
    
    # 3. ВАЛИДАЦИЯ (исключение аномалий)
    valid_prices = validate_prices(competitor_prices)
    # OBI слишком низкий? Исключаем если > 3 сигма
    
    # 4. РАСЧЁТ СТАТИСТИКИ
    avg_price = mean(valid_prices)      # 125р
    min_price = min(valid_prices)       # 110р
    max_price = max(valid_prices)       # 140р
    std_dev = stdev(valid_prices)       # 5р
    
    # 5. АНАЛИЗ MARKET POSITION
    if avg_price > base_price * 1.15:
        # Конкуренты дорогие, можем повысить
        position = "UNDERCUTTING_OPPORTUNITY"
        target_price = avg_price * 0.95  # -5% от среднего
    elif avg_price < base_price * 0.85:
        # Конкуренты дешёвые, нужна подстройка
        position = "COMPETITIVE_PRESSURE"
        target_price = avg_price * 1.02  # +2% от среднего
    else:
        # Конкуренты близко
        position = "EQUILIBRIUM"
        target_price = max(base_price, avg_price * 0.98)
    
    # 6. КОНТРОЛЬ МАРЖИ (абсолютный минимум)
    min_acceptable_price = product.cost_price + MIN_MARGIN_RUB
    final_price = max(target_price, min_acceptable_price)
    # 50р минимум маржи гарантирован
    
    # 7. КОНТРОЛЬ МАКСИМАЛЬНОЙ НАЦЕНКИ
    max_acceptable_price = product.cost_price * (1 + MAX_MARKUP / 100)
    final_price = min(final_price, max_acceptable_price)
    # 30% максимум наценки
    
    # 8. ОКРУГЛЕНИЕ (для красоты)
    final_price = round(final_price, 2)
    
    return {
        "price": final_price,
        "position": position,
        "competitors_avg": avg_price,
        "margin_rub": final_price - product.cost_price,
        "margin_percent": ((final_price - product.cost_price) / product.cost_price) * 100,
        "rank": calculate_rank(final_price, valid_prices),
    }
```

### 6.2 Параметры стратегии (настраиваются)

```python
PRICING_STRATEGY = {
    "MIN_MARKUP": 10,              # Минимальная наценка %
    "MAX_MARKUP": 30,              # Максимальная наценка %
    "MIN_MARGIN_RUB": 50,          # Минимальная маржа в рублях
    
    "COMPETITOR_WEIGHT": 0.7,      # Вес цен конкурентов в алгоритме
    "POPULARITY_WEIGHT": 0.2,      # Вес популярности товара
    "CATEGORY_WEIGHT": 0.1,        # Вес категории
    
    "UNDERCUT_PERCENTAGE": 5,      # На сколько % дешевле конкурентов
    "MATCH_PERCENTAGE": 2,         # На сколько % выше конкурентов
    
    "OUTLIER_STD_DEV": 3,          # Исключить цены > 3 сигма
    "SUSPICIOUS_STD_DEV": 1.5,     # Отметить как подозрительные > 1.5 сигма
    
    "YANDEX_DEVIATION_THRESHOLD": 20,  # Alert если > 20% от Yandex
    "PRICE_UPDATE_THRESHOLD_RUB": 5,   # Обновить если > 5р разница
    "PRICE_UPDATE_THRESHOLD_PERCENT": 2, # Обновить если > 2% разница
}
```

### 6.3 Примеры расчётов

**Пример 1: Кирпич облицовочный**
```
Cost: 15р/шт
Min_margin: 50р
Max_markup: 30%

Конкуренты:
- Петрович: 24р
- Leroy: 26р
- OBI: 23р
- Avangard: 25р
- E-catalog: 24.5р

Средняя: 24.5р
Медиана: 24р

Расчёт:
base_price = 15 × 1.10 = 16.5р
позиция = COMPETITIVE (24.5 близко к 16.5)
target = max(16.5, 24.5 × 0.98) = 24.01р
min_acceptable = 15 + 50 = 65р
FINAL PRICE = max(24.01, 65) = 65р

⚠️ В этом случае маржа растёт!
Маржа: 65 - 15 = 50р ✅
```

---

## 🌐 API

### 7.1 Основные endpoints

```
┌─ КАТАЛОГ ───────────────────────────────┐
GET    /api/products              # Список
GET    /api/products/{id}        # Один товар
POST   /api/products             # Добавить
PUT    /api/products/{id}        # Обновить
DELETE /api/products/{id}        # Удалить
GET    /api/products/search      # Поиск
└─────────────────────────────────────────┘

┌─ АНАЛИЗ РЫНКА ──────────────────────────┐
GET    /api/monitoring/market-analysis/{id}
GET    /api/monitoring/price-ranking/{id}
GET    /api/monitoring/price-history/{id}
GET    /api/monitoring/competitors/{id}
└─────────────────────────────────────────┘

┌─ УПРАВЛЕНИЕ ЦЕНАМИ ─────────────────────┐
GET    /api/pricing/strategy
PUT    /api/pricing/strategy
POST   /api/pricing/calculate-all
POST   /api/pricing/calculate/{id}
└─────────────────────────────────────────┘

┌─ АДМИНИСТРИРОВАНИЕ ─────────────────────┐
GET    /api/admin/sources          # Источники
POST   /api/admin/parse-all        # Парсить всё
POST   /api/admin/parse/{source}   # Парсить конкретный
GET    /api/admin/parse-status
GET    /api/admin/alerts
└─────────────────────────────────────────┘
```

---

## 📅 ПЛАНЫ РАЗВИТИЯ

### Фаза 1: Базовая система (Месяцы 1-2)
- ✅ БД структура
- ✅ Парсеры для 3 основных сайтов (Петрович, Leroy, OBI)
- ✅ Базовый каталог (15,000 товаров)
- ✅ Мониторинг цен (эти 3 источника)
- ✅ Расчёт цен (простая стратегия)
- ✅ API (базовый)
- ✅ Admin Panel (управление)

### Фаза 2: Расширение (Месяцы 3-4)
- Добавить 5 новых источников (20+ источников в total)
- Парсер Yandex Market (с API)
- Расширить каталог до 50,000 товаров
- Продвинутый анализ рынка
- Оповещения
- Экспорт/импорт

### Фаза 3: Оптимизация (Месяцы 5-6)
- Добавить B2B источники (Alibaba, производители)
- Достичь 100+ источников ЦЕН на товар
- Региональная аналитика
- ML-модели для прогнозирования
- Мобильное приложение

---

## 📊 СРОКИ И РЕСУРСЫ

### 9.1 График реализации

```
                │   Фаза 1   │   Фаза 2   │   Фаза 3   │
                │ (1-2 мес)  │ (3-4 мес)  │ (5-6 мес)  │
────────────────┼────────────┼────────────┼────────────┤
БД структура   │ ███████████│            │            │
Парсеры (3)    │ ███████████│            │            │
Парсеры (20)   │            │ ███████████│            │
Парсеры (100)  │            │            │ ███████████│
Каталог        │ ███████████│ ███████████│ ███████████│
Мониторинг     │ ███████████│ ███████████│ ███████████│
Прайсинг       │ ███████████│ ███████████│ ███████████│
API            │ ███████████│ ███████████│ ███████████│
ML модели      │            │            │ ███████████│
```

### 9.2 Требуемые ресурсы

```
ТИМ:
├─ Backend разработчик (Python/FastAPI): 1 основной + 1 помощник
├─ Парсер-специалист (BeautifulSoup/Selenium): 1 person
├─ DevOps (Docker/K8s): 0.5 человека
├─ Product Manager: 1 person
├─ QA / Тестирование: 0.5 человека
└─ Total: 4 человека

ИНФРАСТРУКТУРА:
├─ Сервер (CPU: 16 cores, RAM: 64GB, Storage: 500GB-1TB)
├─ БД (PostgreSQL 14+, Backup, Replication)
├─ Redis (Cache, Queue)
├─ Мониторинг (Prometheus, Grafana)
└─ Стоимость: $1,000-2,000/месяц

ПОСТОЯННЫЕ ЗАТРАТЫ:
├─ Зарплата команды
├─ API ключи для источников
├─ Инфраструктура
├─ Лицензии ПО
└─ Маркетинг/продажи
```

---

## ✅ КРИТЕРИИ УСПЕХА

### 1. Каталог
- ✅ Минимум 15,000 артикулов (к концу Фазы 1)
- ✅ 50,000+ артикулов (к концу Фазы 2)
- ✅ 100,000+ артикулов (к концу Фазы 3)

### 2. Источники ЦЕН
- ✅ 3 основных источника (Фаза 1)
- ✅ 20+ источников (Фаза 2)
- ✅ 100+ источников (Фаза 3)

### 3. Качество данных
- ✅ 95%+ успешных парсингов
- ✅ <5% аномалий в ценах
- ✅ 99.9% uptime системы мониторинга

### 4. Бизнес-метрики
- ✅ Снижение себестоимости на 15-25%
- ✅ Срок окупаемости: <6 месяцев
- ✅ ROI: >300% за год

---

## 🎯 ЗАКЛЮЧЕНИЕ

Данное техническое задание описывает полнофункциональную систему для:
1. **Сбора и анализа** номенклатуры строматериалов
2. **Мониторинга цен** от 100+ поставщиков
3. **Оптимального ценообразования** на основе конкурентного анализа
4. **Рекомендаций по закупкам** для минимизации затрат

Система обеспечит:
- Реальное время данные о рынке
- Автоматическое управление ценами
- Аналитику для закупок
- Конкурентное преимущество

**Статус:** Готовое ТЗ к разработке ✅
**Дата:** 11.01.2026
