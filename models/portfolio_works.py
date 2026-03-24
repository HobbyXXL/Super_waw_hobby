from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base
from datetime import datetime

class PortfolioWork(Base):
    __tablename__ = "portfolio_works"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    file_url = Column(Text)
    visibility = Column(String, default="public")
    created_at = Column(DateTime, default=datetime.utcnow)