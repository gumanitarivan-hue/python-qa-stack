import allure
import pytest

from src.api.models import Order

pytestmark = pytest.mark.api

MISSING_ID = 2_000_000_000


@allure.title("POST /orders создаёт заказ пользователя")
def test_create_order(shop_api, created_user):
    response = shop_api.post("/orders", json={"user_id": created_user["id"], "amount": 10.5})

    assert response.status_code == 201
    order = Order(**response.json())
    assert order.user_id == created_user["id"]
    assert order.amount == 10.5


@allure.title("POST /orders с некорректной суммой возвращает 422")
@pytest.mark.parametrize("amount", [0, -5, "abc"])
def test_create_order_invalid_amount(shop_api, created_user, amount):
    response = shop_api.post("/orders", json={"user_id": created_user["id"], "amount": amount})

    assert response.status_code == 422


@allure.title("POST /orders для несуществующего пользователя возвращает 404")
def test_create_order_unknown_user(shop_api):
    response = shop_api.post("/orders", json={"user_id": MISSING_ID, "amount": 10})

    assert response.status_code == 404


@allure.title("POST /orders с некорректным user_id возвращает 422")
@pytest.mark.parametrize("user_id", [0, -1])
def test_create_order_invalid_user_id(shop_api, user_id):
    response = shop_api.post("/orders", json={"user_id": user_id, "amount": 10})

    assert response.status_code == 422


@allure.title("GET /orders/{id} возвращает заказ")
def test_get_order(shop_api, created_user):
    created = shop_api.post("/orders", json={"user_id": created_user["id"], "amount": 7}).json()

    response = shop_api.get(f"/orders/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


@allure.title("GET несуществующего заказа возвращает 404")
def test_get_missing_order(shop_api):
    response = shop_api.get(f"/orders/{MISSING_ID}")

    assert response.status_code == 404


@allure.title("GET /users/{id}/orders возвращает заказы пользователя")
def test_list_user_orders(shop_api, created_user):
    for amount in (10.5, 4.5):
        shop_api.post("/orders", json={"user_id": created_user["id"], "amount": amount})

    response = shop_api.get(f"/users/{created_user['id']}/orders")

    assert response.status_code == 200
    orders = [Order(**item) for item in response.json()]
    assert len(orders) == 2
    assert sum(order.amount for order in orders) == 15.0


@allure.title("GET /users/{id}/orders для несуществующего пользователя возвращает 404")
def test_list_orders_of_missing_user(shop_api):
    response = shop_api.get(f"/users/{MISSING_ID}/orders")

    assert response.status_code == 404


@allure.title("DELETE /orders/{id} удаляет заказ")
def test_delete_order(shop_api, created_user):
    created = shop_api.post("/orders", json={"user_id": created_user["id"], "amount": 3}).json()

    response = shop_api.delete(f"/orders/{created['id']}")

    assert response.status_code == 204
    assert shop_api.get(f"/orders/{created['id']}").status_code == 404


@allure.title("DELETE несуществующего заказа возвращает 404")
def test_delete_missing_order(shop_api):
    response = shop_api.delete(f"/orders/{MISSING_ID}")

    assert response.status_code == 404
