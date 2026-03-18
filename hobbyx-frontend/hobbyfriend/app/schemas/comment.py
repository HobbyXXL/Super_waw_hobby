# app/schemas/comment.py

from pydantic import BaseModel

# Предполагаем, что здесь определен класс CommentBase
class CommentBase(BaseModel):
    text: str
    user_id: int
    post_id: int

class CommentCreate(CommentBase):
    # Если для создания комментария нужны дополнительные поля, добавь их сюда
    pass

class CommentRead(CommentBase):
    id: int
    # Могут быть добавлены поля для отображения (например, имя пользователя)
    pass

# Также убедись, что в app/schemas/__init__.py есть экспорт этих классов,
# если ты используешь такой подход к организации схем:
# from .comment import CommentCreate, CommentRead
