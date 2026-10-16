from pydantic import BaseModel


class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str
