from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Community(Base):
    __tablename__ = "communities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    slug = Column(String(150), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    is_private = Column(Boolean, default=False)
    creator_id = Column(String(36), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Убери эту строку, если CommunityMember определён отдельно
    # members = relationship("CommunityMember", back_pop