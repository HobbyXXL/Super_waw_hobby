from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, UniqueConstraint
from .base import Base
import enum

class ExperienceLevel(str, enum.Enum):
    """Уровни опыта в хобби"""
    BEGINNER = "beginner"  # Только начал заниматься
    INTERMEDIATE = "intermediate"  # Занимается несколько месяцев, что-то умеет
    ADVANCED = "advanced"  # Продвинутый уровень

class UserHobby(Base):
    __tablename__ = "user_hobbies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    hobby_id = Column(Integer, ForeignKey("hobbies.id"), nullable=False)
    
    experience_level = Column(String, nullable=True)
    
    frequency_per_week = Column(Integer, nullable=True)  # дней в неделю
    frequency_per_month = Column(Integer, nullable=True)  # дней в месяц
    
    experience_description = Column(Text, nullable=True)  # "чем хочешь заниматься"
    why_this_hobby = Column(Text, nullable=True)  # "почему ты хочешь этим заниматься"
    looking_for_in_partner = Column(Text, nullable=True)  # "кого ищет" для этого хобби
    
    is_public = Column(Boolean, default=True)  # публичное или личное
    
    __table_args__ = (
        UniqueConstraint('user_id', 'hobby_id', name='unique_user_hobby'),
    )