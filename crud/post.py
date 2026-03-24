from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Post, Tag, PostTag, Like, Comment
from schemas.post import PostCreate


def create_post(db: Session, post: PostCreate, user_id: int):
    if len(post.tag_ids) > 10:
        raise ValueError("Максимум 10 тегов")

    db_post = Post(**post.dict(exclude={"tag_ids"}), user_id=user_id)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    if post.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(post.tag_ids)).all()
        for tag in tags:
            db.add(PostTag(post_id=db_post.id, tag_id=tag.id))
        db.commit()

    return db_post


def get_feed(db: Session):
    posts = db.query(Post).all()

    result = []
    for p in posts:
        result.append({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "likes": db.query(func.count(Like.id)).filter(Like.post_id == p.id).scalar(),
            "comments": db.query(func.count(Comment.id)).filter(Comment.post_id == p.id).scalar(),
        })

    return result