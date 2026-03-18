from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    author_id = Column(String)
    likes = Column(Integer, default=0)