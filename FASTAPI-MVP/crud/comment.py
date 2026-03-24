from sqlalchemy.orm import Session
from models import Comment


def create_comment(db: Session, user_id: int, post_id: int, content: str):
    comment = Comment(user_id=user_id, post_id=post_id, content=content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment