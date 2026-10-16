import allure
import psycopg
import pytest

pytestmark = pytest.mark.db


def insert_user(db, email):
    return db.execute(
        "INSERT INTO users (email, name) VALUES (%s, 'Test') RETURNING id", (email,)
    ).fetchone()[0]


@allure.title("Email пользователя должен быть уникальным")
def test_email_must_be_unique(db, unique_email):
    insert_user(db, unique_email)

    with pytest.raises(psycopg.errors.UniqueViolation):
        insert_user(db, unique_email)


@allure.title("Имя пользователя не может быть NULL")
def test_name_must_not_be_null(db, unique_email):
    with pytest.raises(psycopg.errors.NotNullViolation):
        db.execute("INSERT INTO users (email, name) VALUES (%s, NULL)", (unique_email,))


@allure.title("Заказ нельзя создать для несуществующего пользователя")
def test_order_requires_existing_user(db):
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        db.execute("INSERT INTO orders (user_id, amount) VALUES (2000000000, 10)")


@allure.title("Сумма заказа должна быть положительной")
@pytest.mark.parametrize("amount", [0, -5])
def test_order_amount_must_be_positive(db, unique_email, amount):
    user_id = insert_user(db, unique_email)

    with pytest.raises(psycopg.errors.CheckViolation):
        db.execute("INSERT INTO orders (user_id, amount) VALUES (%s, %s)", (user_id, amount))


@allure.title("Нельзя удалить пользователя, у которого есть заказы")
def test_cannot_delete_user_with_orders(db, unique_email):
    user_id = insert_user(db, unique_email)
    db.execute("INSERT INTO orders (user_id, amount) VALUES (%s, 10)", (user_id,))

    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        db.execute("DELETE FROM users WHERE id = %s", (user_id,))


@allure.title("JOIN возвращает сумму заказов пользователя")
def test_join_sums_user_orders(db, unique_email):
    user_id = insert_user(db, unique_email)
    db.execute(
        "INSERT INTO orders (user_id, amount) VALUES (%s, 10.50), (%s, 4.50)",
        (user_id, user_id),
    )

    total = db.execute(
        "SELECT SUM(o.amount) FROM orders o JOIN users u ON u.id = o.user_id WHERE u.email = %s",
        (unique_email,),
    ).fetchone()[0]

    assert total == 15
