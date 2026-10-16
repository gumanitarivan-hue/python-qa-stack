"""Небольшое приложение: пользователи и заказы. Объект тестирования."""

import os
from collections.abc import Iterator

import psycopg
from fastapi import Depends, FastAPI, HTTPException, Response
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from psycopg.rows import dict_row
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="QA Demo Shop API")

MAX_INT4 = 2_147_483_647


def get_conn() -> Iterator[psycopg.Connection]:
    # autocommit: каждый запрос сразу фиксируется в БД
    with psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        autocommit=True,
        row_factory=dict_row,
    ) as conn:
        yield conn


class UserIn(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)


class UserOut(BaseModel):
    id: int
    email: str
    name: str


class OrderIn(BaseModel):
    user_id: int = Field(gt=0, le=MAX_INT4)
    amount: float = Field(gt=0, le=1_000_000)


class OrderOut(BaseModel):
    id: int
    user_id: int
    amount: float


def to_order(row: dict) -> dict:
    # в БД сумма хранится как NUMERIC; для простоты отдаём float
    return {**row, "amount": float(row["amount"])}


@app.get("/health")
def health(conn=Depends(get_conn)):
    conn.execute("SELECT 1")
    return {"status": "ok"}


@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn, conn=Depends(get_conn)):
    try:
        return conn.execute(
            "INSERT INTO users (email, name) VALUES (%s, %s) RETURNING id, email, name",
            (user.email, user.name),
        ).fetchone()
    except UniqueViolation:
        raise HTTPException(status_code=409, detail="Email already exists") from None


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, conn=Depends(get_conn)):
    row = conn.execute(
        "SELECT id, email, name FROM users WHERE id = %s", (user_id,)
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return row


@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order: OrderIn, conn=Depends(get_conn)):
    try:
        row = conn.execute(
            "INSERT INTO orders (user_id, amount) VALUES (%s, %s) "
            "RETURNING id, user_id, amount",
            (order.user_id, order.amount),
        ).fetchone()
    except ForeignKeyViolation:
        raise HTTPException(status_code=404, detail="User not found") from None
    return to_order(row)


@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, conn=Depends(get_conn)):
    row = conn.execute(
        "SELECT id, user_id, amount FROM orders WHERE id = %s", (order_id,)
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return to_order(row)


@app.get("/users/{user_id}/orders", response_model=list[OrderOut])
def list_user_orders(user_id: int, conn=Depends(get_conn)):
    get_user(user_id, conn)  # 404, если пользователя нет
    rows = conn.execute(
        "SELECT id, user_id, amount FROM orders WHERE user_id = %s ORDER BY id",
        (user_id,),
    ).fetchall()
    return [to_order(r) for r in rows]


@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int, conn=Depends(get_conn)):
    row = conn.execute(
        "DELETE FROM orders WHERE id = %s RETURNING id", (order_id,)
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return Response(status_code=204)