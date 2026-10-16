import allure
import pytest

from src.api.models import User

pytestmark = pytest.mark.api


@allure.title("POST /users создаёт пользователя")
def test_create_user(shop_api, unique_email):
    response = shop_api.post("/users", json={"email": unique_email, "name": "Anna"})

    assert response.status_code == 201
    user = User(**response.json())
    assert user.email == unique_email
    assert user.name == "Anna"
    assert user.id > 0


@allure.title("POST /users с повторным email возвращает 409")
def test_create_user_duplicate_email(shop_api, created_user):
    response = shop_api.post("/users", json={"email": created_user["email"], "name": "Another"})

    assert response.status_code == 409


@allure.title("POST /users с некорректным email возвращает 422")
@pytest.mark.parametrize("email", ["not-an-email", "a@", "@example.com", ""])
def test_create_user_invalid_email(shop_api, email):
    response = shop_api.post("/users", json={"email": email, "name": "Anna"})

    assert response.status_code == 422


@allure.title("POST /users с некорректным именем возвращает 422")
@pytest.mark.parametrize("name", ["", "x" * 101])
def test_create_user_invalid_name(shop_api, unique_email, name):
    response = shop_api.post("/users", json={"email": unique_email, "name": name})

    assert response.status_code == 422


@allure.title("POST /users без имени возвращает 422")
def test_create_user_without_name(shop_api, unique_email):
    response = shop_api.post("/users", json={"email": unique_email})

    assert response.status_code == 422


@allure.title("GET /users/{id} возвращает созданного пользователя")
def test_get_user(shop_api, created_user):
    response = shop_api.get(f"/users/{created_user['id']}")

    assert response.status_code == 200
    assert response.json() == created_user


@allure.title("GET несуществующего пользователя возвращает 404")
@pytest.mark.parametrize("user_id", [0, -1, 2_000_000_000])
def test_get_missing_user(shop_api, user_id):
    response = shop_api.get(f"/users/{user_id}")

    assert response.status_code == 404


@allure.title("GET /users/abc возвращает 422")
def test_get_user_non_numeric_id(shop_api):
    response = shop_api.get("/users/abc")

    assert response.status_code == 422
