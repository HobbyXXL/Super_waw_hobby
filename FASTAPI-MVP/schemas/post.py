from pydantic import BaseModel
from typing import List, Optional


class PostCreate(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    hobby_done: bool = False
    tag_ids: List[int] = []


class PostRead(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True