from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from .base import Base
from datetime import datetime, timedelta

class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    code = Column(String(6), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)
    
    # ✅ НОВОЕ: Временное хранение данных регистрации
    temp_login = Column(String, nullable=True)
    temp_password_hash = Column(String, nullable=True)
    temp_role = Column(String, default="user", nullable=True)

    @classmethod
    def generate_expires_at(cls, minutes: int = 15) -> datetime:
        """Генерирует время истечения кода (по умолчанию 15 минут)"""
        return datetime.utcnow() + timedelta(minutes=minutes)

    @classmethod
    def generate_code(cls) -> str:
        """Генерирует 6-значный код подтверждения"""
        import random
        return str(random.randint(100000, 999999))