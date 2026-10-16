from decimal import Decimal

import allure
import pytest

pytestmark = pytest.mark.db


@allure.title("Пользователь, созданный через API, есть в БД")
def test_user_created_via_api_is_in_db(shop_api, db, unique_email):
    response = shop_api.post("/users", json={"email": unique_email, "name": "Anna"})
    user_id = response.json()["id"]

    row = db.execute("SELECT email, name FROM users WHERE id = %s", (user_id,)).fetchone()

    assert row == (unique_email, "Anna")


@allure.title("Заказ, созданный через API, сохраняется в БД с верной суммой")
def test_order_created_via_api_is_in_db(shop_api, db, created_user):
    response = shop_api.post("/orders", json={"user_id": created_user["id"], "amount": 10.5})
    order_id = response.json()["id"]

    row = db.execute("SELECT user_id, amount FROM orders WHERE id = %s", (order_id,)).fetchone()

    assert row == (created_user["id"], Decimal("10.50"))


@allure.title("Заказ, удалённый через API, пропадает из БД")
def test_order_deleted_via_api_is_gone_from_db(shop_api, db, created_user):
    order = shop_api.post("/orders", json={"user_id": created_user["id"], "amount": 3}).json()

    shop_api.delete(f"/orders/{order['id']}")

    count = db.execute("SELECT count(*) FROM orders WHERE id = %s", (order["id"],)).fetchone()[0]
    assert count == 0
