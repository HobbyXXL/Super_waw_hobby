from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class CommunityMember(Base):
    __tablename__ = "community_members"
    __table_args__ = {'extend_existing': True}  # ✅ Добавь эту строку

    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("communities.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), nullable=False)
    role = Column(String(30), default="member")
    joined_at = Column(DateTime(timezone=True), server_default=func.now())