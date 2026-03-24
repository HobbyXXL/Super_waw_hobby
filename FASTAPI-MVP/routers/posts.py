from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.post import PostCreate
from crud.post import create_post, get_feed

router = APIRouter(
    prefix="/posts",
    tags=["📄 Посты"]
)


@router.post(
    "/",
    summary="✍️ Создать пост",
    description="Создаёт новый пост с текстом, изображением и тегами"
)
def create_post_endpoint(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post, user_id=1)


@router.get(
    "/",
    summary="📰 Лента постов",
    description="Возвращает список всех постов с количеством лайков и комментариев"
)
def get_posts(db: Session = Depends(get_db)):
    return get_feed(db)