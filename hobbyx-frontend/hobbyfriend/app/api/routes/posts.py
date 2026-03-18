from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db_dep, get_current_user
from app.services.post_service import PostService
from app.api.deps import get_db
from fastapi import APIRouter, Depends
from app.models.post import Post

router = APIRouter(prefix="/posts", tags=["posts"])
@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

@router.post("/")
def create_post(data: dict, db: Session = Depends(get_db_dep), user=Depends(get_current_user)):
    return PostService(db).create_post(user.id, data)

@router.post("/{post_id}/like")
def like(post_id: int, db: Session = Depends(get_db_dep), user=Depends(get_current_user)):
    return PostService(db).toggle_like(post_id, user.id)

@router.post("/{post_id}/comments")
def comment(post_id: int, data: dict, db: Session = Depends(get_db_dep), user=Depends(get_current_user)):
    return PostService(db).add_comment(post_id, user.id, data)