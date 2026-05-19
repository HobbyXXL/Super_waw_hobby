from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .base import Base

class UserGoal(Base):
    __tablename__ = "user_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    is_completed = Column(Boolean, default=False)