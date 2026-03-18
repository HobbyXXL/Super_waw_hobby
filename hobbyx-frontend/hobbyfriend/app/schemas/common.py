from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CommentBase(BaseModel):
    content: str
    parent_id: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
    author_id: str
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True