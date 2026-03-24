from sqlalchemy.orm import Session
from models import Like


def toggle_like(db: Session, user_id: int, post_id: int):
    like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == post_id
    ).first()

    if like:
        db.delete(like)
        db.commit()
        return {"status": "unliked"}

    db.add(Like(user_id=user_id, post_id=post_id))
    db.commit()
    return {"status": "liked"}


def get_liked_posts(db: Session, user_id: int):
    return db.query(Like).filter(Like.user_id == user_id).all()