from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from crud.comment import create_comment

router = APIRouter(
    prefix="/comments",
    tags=["💬 Комментарии"]
)


@router.post(
    "/{post_id}",
    summary="💬 Добавить комментарий",
    description="Добавляет комментарий к выбранному посту"
)
def add_comment(post_id: int, content: str, db: Session = Depends(get_db)):
    return create_comment(db, user_id=1, post_id=post_id, content=content)