# Python QA Automation Stack

[![Tests](https://github.com/gumanitarivan-hue/python-qa-stack/actions/workflows/tests.yml/badge.svg)](https://github.com/gumanitarivan-hue/python-qa-stack/actions/workflows/tests.yml)
[![Allure report](https://img.shields.io/badge/Allure-report-blueviolet)](https://gumanitarivan-hue.github.io/python-qa-stack/)

Демонстрационный проект по автоматизации тестирования на Python: тестируемое
приложение (пользователи и заказы), три слоя автотестов (API, БД, UI),
запуск в Docker и CI с публикацией Allure-отчёта.

**[Последний Allure-отчёт](https://gumanitarivan-hue.github.io/python-qa-stack/)**

## Что внутри

| Слой | Что проверяется | Инструменты |
|------|-----------------|-------------|
| API | CRUD, валидация (422), дубликаты (409), связи между сущностями, схемы ответов | requests, pydantic |
| БД | UNIQUE, NOT NULL, FOREIGN KEY, CHECK, JOIN; запись через API видна в БД | psycopg, SQL |
| UI | вход, каталог, сортировка, корзина, оформление заказа (Page Object) | Playwright |

Более 70 тестов. Тестируемое приложение (`app/`) написано на FastAPI и хранит
данные в PostgreSQL. UI-тесты идут по демо-магазину saucedemo.com, а набор
тестов на публичный JSONPlaceholder показывает работу с внешним API.

## Структура проекта

```
app/                 тестируемое приложение (FastAPI + PostgreSQL)
db/init.sql          схема БД, создаётся при старте контейнера
src/
  api/               HTTP-клиент и pydantic-модели ответов
  pages/             Page Object для UI
  config.py          настройки из переменных окружения / .env
tests/
  api/  db/  ui/     тесты по слоям
  conftest.py        общие фикстуры
.github/workflows/   CI
compose.yaml         приложение + БД + контейнер с тестами
```

## Запуск локально

Нужны Python 3.12+ и Docker.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
Copy-Item .env.example .env           # Linux/macOS: cp .env.example .env
docker compose up -d --build --wait   # приложение и БД
pytest
```

Часть тестов по маркерам: `pytest -m api`, `pytest -m db`, `pytest -m ui`.
Параллельно: `pytest -n 2`.

## Запуск в Docker

```powershell
docker compose run --build --rm tests
docker compose down -v
```

Результаты (`allure-results/`, трейсы упавших UI-тестов в `test-results/`)
сохраняются на диск.

## CI

GitHub Actions при каждом пуше и pull request:

1. **Lint:** `ruff check` и `ruff format --check`.
2. **Tests:** поднимает приложение и БД через Docker Compose, запускает все тесты
   параллельно, сохраняет результаты и трейсы упавших тестов.
3. **Allure report:** собирает отчёт; для ветки `main` публикует его на GitHub Pages.

### Jenkins (локально)

В репозитории есть `Jenkinsfile` (стадии Lint и Tests) и конфигурация для
локального запуска Jenkins в Docker:
`docker compose -f jenkins/compose.yaml up -d --build`.
Основной CI проекта: GitHub Actions. Jenkins запускается вручную.

## Ключевые решения

- **Независимые тесты.** Каждый тест создаёт данные с уникальным email,
  поэтому базу не нужно чистить и тесты можно запускать параллельно.
- **Page Object и фикстуры.** Локаторы и шаги живут в `src/pages/`, настройка
  состояния (логин, корзина) в фикстурах, а в самих тестах остаётся сценарий.
- **Схемы ответов** проверяются через pydantic, поэтому лишнее или пропавшее
  поле ловится сразу.
- **Повторы** (`pytest-rerunfailures`) включены только для тестов, зависящих от
  внешних сайтов (UI и JSONPlaceholder). Тесты собственного приложения не
  перезапускаются, чтобы не скрывать реальные дефекты.
- **Секреты** не хранятся в коде: настройки идут через `.env` (в git только
  `.env.example`).

## Упрощения

Приложение демонстрационное: нет авторизации, а сумма заказа хранится как
`float` (в реальной системе нужен `Decimal` или целые копейки). Сайты
saucedemo.com и JSONPlaceholder сторонние, поэтому при их сбоях возможны
ложные падения.

## Автор

Тимур Б-aka-ChubbyTim-akagumanitarivan.
Контакты: tg:@ragazzomisterioso