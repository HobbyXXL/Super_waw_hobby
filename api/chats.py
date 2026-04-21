from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from database import get_db
from dependency import get_current_user
from models import User as UserModel, Chat as ChatModel
from services.chats import ChatService
from schemas import Chat, ChatCreate, ChatList, Message, MessageCreate

# ← ВАЖНО: Создаём router!
router = APIRouter(prefix="/chats", tags=["Chats"])

#  ЧАТ: Создать или получить 
@router.post("/", response_model=Chat, status_code=status.HTTP_201_CREATED)
def create_or_get_chat(
    chat: ChatCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Создать новый чат или получить существующий"""
    if chat.user2_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot create chat with yourself")
    
    service = ChatService(db)
    return service.get_or_create_chat(current_user.id, chat.user2_id)

# Список всех чатов 
@router.get("/", response_model=list[ChatList])
def get_my_chats(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Получить все мои чаты"""
    service = ChatService(db)
    return service.get_user_chats(current_user.id)

@router.post("/{chat_id}/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
def send_message(
    chat_id: int,
    message_data: MessageCreate = Body(...), 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Отправить сообщение в чат"""
    service = ChatService(db)
    try:
        return service.send_message(chat_id, current_user.id, message_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

#  СООБЩЕНИЯ: Получить все сообщения 
@router.get("/{chat_id}/messages", response_model=list[Message])
def get_chat_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Получить все сообщения в чате"""
    service = ChatService(db)
    try:
        return service.get_chat_messages(chat_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

#  ЧАТ: Получить конкретный чат 
@router.get("/{chat_id}", response_model=Chat)
def get_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Получить информацию о чате"""
    chat = db.query(ChatModel).filter(
        (ChatModel.id == chat_id) & (
            (ChatModel.user1_id == current_user.id) | (ChatModel.user2_id == current_user.id)
        )
    ).first()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return chat