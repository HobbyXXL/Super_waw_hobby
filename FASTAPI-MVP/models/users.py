from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from .base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    is_blocked = Column(Boolean, default=False)
    terms_version_id = Column(Integer, ForeignKey("terms_versions.id"))
    created_at = Column(DateTime, default=datetime.utcnow)