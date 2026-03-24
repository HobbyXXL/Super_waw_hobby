from sqlalchemy import Column, String, Integer, ForeignKey
from database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    display_name = Column(String, nullable=False)
    age = Column(Integer)
    city = Column(String)
    avatar_url = Column(String)