from sqlalchemy.orm import Session
from models.comments import Comment
from models.users import User
from models.portfolio_works import PortfolioWork


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_post(self, post_id: int) -> PortfolioWork | None:
        return (
            self.db.query(PortfolioWork)
            .filter(PortfolioWork.id == post_id, PortfolioWork.is_active == True)
            .first()
        )

    def list_for_post(self, post_id: int) -> list[tuple[Comment, User]]:
        return (
            self.db.query(Comment, User)
            .join(User, Comment.user_id == User.id)
            .filter(Comment.post_id == post_id)
            .order_by(Comment.created_at.asc())
            .all()
        )

    def create(self, post_id: int, user_id: str, body: str) -> Comment:
        comment = Comment(post_id=post_id, user_id=user_id, body=body)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_with_author(self, comment_id: int) -> tuple[Comment, User] | None:
        row = (
            self.db.query(Comment, User)
            .join(User, Comment.user_id == User.id)
            .filter(Comment.id == comment_id)
            .first()
        )
        return row
