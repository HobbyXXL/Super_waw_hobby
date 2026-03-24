from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    post = relationship("Post", back_populates="comments")