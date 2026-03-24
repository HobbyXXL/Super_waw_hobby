from app.database import SessionLocal
from app.models import Tag, Post, User, PostTag
from sqlalchemy import select

db = SessionLocal()

tags = ["Спорт", "Рисование", "Музыка", "Кулинария", "Программирование", "Чтение", "Танцы", "Фотография", "Путешествия", "Рукоделие"]
for t in tags:
    if not db.execute(select(Tag).where(Tag.name == t)).scalar():
        db.add(Tag(name=t))
db.commit()

user = db.query(User).first()  # берём первого юзера
if not user:
    print("Создай хотя бы одного пользователя через /users/")
    exit()

post1 = Post(
    title="Мой первый пост",
    content="Сегодня занимался хобби!",
    hobby_done=True,
    user_id=user.id,
    image_url="https://picsum.photos/400/300"
)
post2 = Post(
    title="Второй пост",
    content="Просто текст без картинки",
    hobby_done=False,
    user_id=user.id
)

db.add_all([post1, post2])
db.commit()

db.close()
print("Тестовые посты и теги добавлены")