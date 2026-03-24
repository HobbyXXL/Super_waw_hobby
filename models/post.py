from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    hobby_done: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship("User", back_populates="posts")
    post_tags = relationship("PostTag", back_populates="post", cascade="all, delete")
    likes = relationship("Like", back_populates="post", cascade="all, delete")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")