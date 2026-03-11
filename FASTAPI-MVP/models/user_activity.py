from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .base import Base

class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    hobby_id = Column(Integer, ForeignKey("hobbies.id"), nullable=False)
    activity_date = Column(Date, nullable=False)
    duration_minutes = Column(Integer, default=0)
