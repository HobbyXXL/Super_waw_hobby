from pydantic import BaseModel, Field
from datetime import datetime


class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=2000)


class CommentAuthor(BaseModel):
    id: str
    login: str

    class Config:
        from_attributes = True


class CommentSchema(BaseModel):
    id: int
    post_id: int
    user_id: str
    body: str
    created_at: datetime
    author: CommentAuthor | None = None

    class Config:
        from_attributes = True
