from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    avatar_url: Mapped[str | None] = mapped_column(String)

    posts = relationship("Post", back_populates="user")
    likes = relationship("Like", back_populates="user")