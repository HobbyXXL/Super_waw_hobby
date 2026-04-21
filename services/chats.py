from sqlalchemy.orm import Session
from models import Chat, User as UserModel
from models.messages import Message as MessageModel  
from schemas import ChatCreate, MessageCreate, ChatList, Message as MessageSchema  # ← Схема
from sqlalchemy import and_, desc

class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_chat(self, user1_id: str, user2_id: str) -> Chat:
        """Получить существующий чат или создать новый"""
        existing_chat = self.db.query(Chat).filter(
            and_(
                ((Chat.user1_id == user1_id) & (Chat.user2_id == user2_id)) |
                ((Chat.user1_id == user2_id) & (Chat.user2_id == user1_id))
            )
        ).first()
        
        if existing_chat:
            return existing_chat
        
        chat = Chat(user1_id=user1_id, user2_id=user2_id)
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def get_user_chats(self, user_id: str) -> list[ChatList]:
        """Получить все чаты пользователя"""
        chats = self.db.query(Chat).filter(
            (Chat.user1_id == user_id) | (Chat.user2_id == user_id)
        ).order_by(desc(Chat.created_at)).all()
        
        result = []
        for chat in chats:
            partner_id = chat.user2_id if chat.user1_id == user_id else chat.user1_id
            partner = self.db.query(UserModel).filter(UserModel.id == partner_id).first()
            
            # ← ИСПРАВЛЕНО: MessageModel вместо Message
            last_message = self.db.query(MessageModel).filter(
                MessageModel.chat_id == chat.id
            ).order_by(desc(MessageModel.sent_at)).first()
            
            # ← ИСПРАВЛЕНО: MessageModel вместо Message
            unread = self.db.query(MessageModel).filter(
                MessageModel.chat_id == chat.id,
                MessageModel.user_id != user_id
            ).order_by(desc(MessageModel.sent_at)).limit(5).count()
            
            chat_list = ChatList(
                id=chat.id,
                user1_id=chat.user1_id,
                user2_id=chat.user2_id,
                created_at=chat.created_at,
                partner_login=partner.login if partner else "Unknown",
                last_message=last_message.body if last_message else None,
                last_message_at=last_message.sent_at if last_message else None,
                unread_count=unread
            )
            result.append(chat_list)
        
        return result

    def get_chat_messages(self, chat_id: int, user_id: str) -> list[MessageSchema]:
        """Получить все сообщения в чате"""
        chat = self.db.query(Chat).filter(
            (Chat.id == chat_id) & (
                (Chat.user1_id == user_id) | (Chat.user2_id == user_id)
            )
        ).first()
        
        if not chat:
            raise ValueError("Chat not found or access denied")
        
        
        messages = self.db.query(MessageModel).filter(
            MessageModel.chat_id == chat_id
        ).order_by(MessageModel.sent_at.asc()).all()
        
        
        return [MessageSchema.model_validate(msg) for msg in messages]

    def send_message(self, chat_id: int, user_id: str, message: MessageCreate) -> MessageSchema:
        """Отправить сообщение в чат"""
        chat = self.db.query(Chat).filter(
            (Chat.id == chat_id) & (
                (Chat.user1_id == user_id) | (Chat.user2_id == user_id)
            )
        ).first()
        
        if not chat:
            raise ValueError("Chat not found or access denied")
        

        db_message = MessageModel(
            chat_id=chat_id,
            user_id=user_id,
            body=message.body
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        

        return MessageSchema.model_validate(db_message)