from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class HobbyBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    category: str = Field(max_length=50)
    description: Optional[str] = Field(None, max_length=255)

class HobbyCreate(HobbyBase):
    pass

class Hobby(HobbyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True