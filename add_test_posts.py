from database import SessionLocal
from models import Post

db = SessionLocal()

db.add(Post(title="Тестовый пост 1", content="Занимался сегодня программированием!", hobby_done=True, user_id=1))
db.add(Post(title="Тестовый пост 2", content="Просто рисую котиков", hobby_done=False, user_id=1))

db.commit()
db.close()

print("Добавлено 2 тестовых поста")