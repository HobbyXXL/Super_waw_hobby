from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.chat_service import ChatService
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.post("/{chat_id}/message")
def send_message(chat_id: int, content: str = None, post_id: int = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ChatService(db).create_message(chat_id, user.id, content, post_id)