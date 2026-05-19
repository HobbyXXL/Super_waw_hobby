from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Boolean
from .base import Base
from datetime import datetime

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    type = Column(String, nullable=False)  
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    why_goal = Column(Text, nullable=True)  
    is_public = Column(Boolean, default=True) 
    
    target_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)