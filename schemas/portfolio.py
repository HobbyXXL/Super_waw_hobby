from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PortfolioWorkBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    file_url: Optional[str] = None  # ← ДОБАВЛЕНО
    visibility: str = Field(default="public")

class PortfolioWorkCreate(PortfolioWorkBase):
    pass

class PortfolioWork(PortfolioWorkBase):
    id: int
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class PortfolioWorkUpload(BaseModel):
    """Схема для создания поста без файла (только текст)"""
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    visibility: str = Field(default="public")

class LikeBase(BaseModel):
    pass

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    id: int
    user_id: str
    portfolio_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class LikeResponse(BaseModel):
    """Ответ при лайке/анлайке"""
    liked: bool
    total_likes: int

class PortfolioWorkBase(BaseModel):
    title: str
    description: str
    activity_status: str = "did_hobby"  # ← ДОБАВЛЕНО

class PortfolioWorkCreate(PortfolioWorkBase):
    file_url: Optional[str] = None
    visibility: str = "public"

class PortfolioWork(PortfolioWorkBase):
    id: int
    user_id: str
    file_url: Optional[str] = None
    visibility: str
    created_at: datetime

    class Config:
        from_attributes = True