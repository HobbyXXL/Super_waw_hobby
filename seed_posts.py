from database import SessionLocal
from models import Post, Tag, User

db = SessionLocal()

# тестовый пользователь
user = db.query(User).first()
if not user:
    user = User(username="testuser", email="test@test.com")
    db.add(user)
    db.commit()
    db.refresh(user)

# теги
for name in ["Спорт", "Рисование", "Музыка", "Кулинария", "Программирование"]:
    if not db.query(Tag).filter(Tag.name == name).first():
        db.add(Tag(name=name))
db.commit()

# посты
post1 = Post(
    title="Пробежал 10 км",
    content="Сегодня прям огонь был!",
    hobby_done=True,
    user_id=user.id,
    image_url="https://picsum.photos/400/300"
)
post2 = Post(
    title="Нарисовал закат",
    content="Просто для души",
    hobby_done=False,
    user_id=user.id
)
db.add_all([post1, post2])
db.commit()

print("Тестовые данные добавлены!")
db.close()