from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Hobby(Base):
    __tablename__ = "hobbies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
