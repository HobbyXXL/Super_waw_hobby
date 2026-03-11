from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    email: str = Field(max_length=100)
    role: str = Field(default="user", max_length=20)

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)

class User(UserBase):
    id: str
    created_at: datetime
    terms_version_id: Optional[int] = None

    class Config:
        from_attributes = True
