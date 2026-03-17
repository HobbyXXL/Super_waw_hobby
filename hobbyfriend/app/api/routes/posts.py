from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db_dep, get_current_user
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/")
def create_post(data: dict, db: Session = Depends(get_db_dep), user=Depends(get_current_user)):
    return PostService(db).create_post(user.id, data)

@router.get("/feed")
def feed(db: Session = Depends(get_db_dep), user=Depends(get_current_user)):
    return PostService(db).get_feed(user.id)

@router.post("/{post_id}/like")
def like(post_id: int, db: Session = Depends(get_db_dep), user=Depends(get_current_user)):
    return PostService(db).toggle_like(post_id, user.id)

@router.post("/{post_id}/comments")
def comment(post_id: int, data: dict, db: Session = Depends(get_db_dep), user=Depends(get_current_user)):
    return PostService(db).add_comment(post_id, user.id, data)