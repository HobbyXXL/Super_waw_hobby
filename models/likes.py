from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from .base import Base
from datetime import datetime

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    portfolio_id = Column(Integer, ForeignKey("portfolio_works.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Один пользователь может лайкнуть пост только один раз
    __table_args__ = (
        UniqueConstraint('user_id', 'portfolio_id', name='unique_user_portfolio_like'),
    )