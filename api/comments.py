from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from dependency import get_current_user
from models.users import User
from repositories.comments import CommentRepository
from services.comments import CommentService
from schemas.comments import CommentCreate, CommentSchema

router = APIRouter(prefix="/posts", tags=["Comments"])


def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(CommentRepository(db))


@router.get("/{post_id}/comments", response_model=list[CommentSchema])
def get_comments(
    post_id: int,
    service: CommentService = Depends(get_comment_service),
):
    return service.list_comments(post_id)


@router.post("/{post_id}/comments", response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    payload: CommentCreate,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(get_comment_service),
):
    return service.add_comment(post_id, current_user.id, payload.body)
