import uuid

import psycopg
import pytest

from src.api.client import ApiClient
from src.config import settings

JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api():
    """Клиент публичного JSONPlaceholder."""
    with ApiClient(JSONPLACEHOLDER_URL) as client:
        yield client


@pytest.fixture(scope="session")
def shop_api():
    """Клиент нашего приложения."""
    with ApiClient(settings.app_url) as client:
        yield client


@pytest.fixture(scope="session")
def db():
    """Подключение к Postgres (autocommit: изменения сразу видны всем)."""
    with psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        autocommit=True,
    ) as conn:
        yield conn


@pytest.fixture
def unique_email():
    """Уникальный email: тесты не мешают друг другу и не требуют очистки БД."""
    return f"user_{uuid.uuid4().hex[:12]}@example.com"


@pytest.fixture
def created_user(shop_api, unique_email):
    """Пользователь, созданный через API."""
    response = shop_api.post("/users", json={"email": unique_email, "name": "Test User"})
    assert response.status_code == 201
    return response.json()
