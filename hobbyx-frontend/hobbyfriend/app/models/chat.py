from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_group = Column(Boolean, default=True)
    members = relationship("ChatMember", back_populates="chat")
    messages = relationship("Message", back_populates="chat")

class ChatMember(Base):
    __tablename__ = "chat_members"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(String, ForeignKey("users.id"))
    chat = relationship("Chat", back_populates="members")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(String, ForeignKey("users.id"))
    content = Column(Text, nullable=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)  # пересылка поста
    created_at = Column(DateTime, default=datetime.utcnow)
    chat = relationship("Chat", back_populates="messages")