from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class UserHobby(Base):
    __tablename__ = "user_hobbies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    hobby_id = Column(Integer, ForeignKey("hobbies.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"))