from sqlalchemy import Column, Integer, String, Text, DateTime
from .base import Base
from datetime import datetime

class Hobby(Base):
    __tablename__ = "hobbies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    
    beginner_description = Column(Text, nullable=True)  # Что значит "начинающий"
    intermediate_description = Column(Text, nullable=True)  # Что значит "средний"
    advanced_description = Column(Text, nullable=True)  # Что значит "продвинутый"
    
    created_at = Column(DateTime, default=datetime.utcnow)