from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from .base import Base
from datetime import datetime

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    hobby_id = Column(Integer, ForeignKey("hobbies.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    title = Column(String)
    links = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
