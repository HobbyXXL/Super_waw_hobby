from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from crud.like import toggle_like, get_liked_posts

router = APIRouter(
    prefix="/likes",
    tags=["❤️ Лайки"]
)


@router.post(
    "/{post_id}",
    summary="❤️ Лайк / убрать лайк",
    description="Ставит или убирает лайк с поста (toggle)"
)
def like_toggle(post_id: int, db: Session = Depends(get_db)):
    return toggle_like(db, user_id=1, post_id=post_id)


@router.get(
    "/",
    summary="⭐ Понравившиеся посты",
    description="Возвращает список постов, которые пользователь лайкнул"
)
def liked_posts(db: Session = Depends(get_db)):
    return get_liked_posts(db, user_id=1)