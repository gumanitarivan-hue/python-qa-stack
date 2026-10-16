from pydantic import BaseModel


class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str


class User(BaseModel):
    id: int
    email: str
    name: str


class Order(BaseModel):
    id: int
    user_id: int
    amount: float
