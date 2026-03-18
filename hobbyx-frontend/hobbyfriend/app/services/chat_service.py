class ChatService:
    def __init__(self, db):
        self.db = db

    def create_message(self, chat_id, user_id, content=None, post_id=None):
        from app.models.chat import Message
        message = Message(chat_id=chat_id, user_id=user_id, content=content, post_id=post_id)
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message