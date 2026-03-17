from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostCreate(BaseModel):
    title: Optional[str] = None
    content: str

class PostRead(BaseModel):
    id: int
    title: Optional[str]
    content: str
    created_at: datetime