from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# === Chat Schemas ===

class ChatBase(BaseModel):
    user2_id: str  # ID пользователя, с которым создаём чат

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int
    user1_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatList(Chat):
    """Чат с информацией о собеседнике"""
    partner_login: Optional[str] = None
    last_message: Optional[str] = None
    last_message_at: Optional[datetime] = None
    unread_count: int = 0

class MessageBase(BaseModel):
    body: str = Field(..., min_length=1, max_length=2000)

class MessageCreate(MessageBase): 
    pass

class Message(MessageBase):  
    id: int
    chat_id: int
    user_id: str
    sent_at: datetime

    class Config:
        from_attributes = True