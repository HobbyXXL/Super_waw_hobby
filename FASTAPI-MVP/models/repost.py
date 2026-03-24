from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Repost(Base):
    __tablename__ = "reposts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))

    #post = relationship("Post", back_populates="likes")
    #user = relationship("User", back_populates="likes")

    __table_args__ = (UniqueConstraint("user_id", "post_id", name="unique_repost"),)