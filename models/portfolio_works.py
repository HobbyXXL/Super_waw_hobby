from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from .base import Base
from datetime import datetime
import enum

class ActivityStatus(str, enum.Enum):
    """Статусы активности пользователя"""
    DID_HOBBY = "did_hobby"  # занимался хобби (зелёный)
    DIDNT_HOBBY = "didnt_hobby"  # не занимался (красный)
    RETURNING = "returning"  # возвращаюсь после паузы (синий)

class PortfolioWork(Base):
    __tablename__ = "portfolio_works"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    hobby_id = Column(Integer, ForeignKey("hobbies.id"), nullable=True)
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    file_url = Column(Text, nullable=True)  # Ссылка на файл/изображение
    
    is_public = Column(Boolean, default=True)  # публичный или личный
    
    visibility = Column(String, default="public")  # legacy поле
    activity_status = Column(String, default=ActivityStatus.DID_HOBBY.value)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)