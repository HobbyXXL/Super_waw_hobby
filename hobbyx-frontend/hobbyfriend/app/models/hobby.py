from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Hobby(Base):
    __tablename__ = "hobbies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)