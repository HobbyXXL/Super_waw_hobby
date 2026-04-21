from sqlalchemy import Column, Integer, String
from .base import Base

class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    min_hours = Column(Integer)