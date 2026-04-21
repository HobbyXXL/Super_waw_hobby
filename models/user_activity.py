from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean
from .base import Base
from datetime import datetime
import enum

class ActivityType(str, enum.Enum):
    """Типы активности в календаре"""
    DID_HOBBY = "did_hobby"  # Занимался хобби (зелёный)
    POST_PUBLISHED = "post_published"  # Опубликовал пост (синий)

class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    hobby_id = Column(Integer, ForeignKey("hobbies.id"), nullable=True)  # nullable, т.к. пост может быть без хобби
    
    activity_type = Column(String, default=ActivityType.DID_HOBBY.value, nullable=False)
    
    post_id = Column(Integer, ForeignKey("portfolio_works.id"), nullable=True)
    
    activity_date = Column(Date, nullable=False, index=True)
    duration_minutes = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)