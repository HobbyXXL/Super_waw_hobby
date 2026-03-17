from app.core.database import get_db
from app.models.user import User
from app.models.post import Post
from app.models.hobby import Hobby
from app.core.security import hash_password

def seed():
    db = next(get_db())

    if db.query(User).first():
        return

    user = User(
        id="u1",
        login="demo",
        email="demo@mail.com",
        hashed_password=hash_password("123456")
    )

    hobby = Hobby(name="Футбол", category="Спорт")

    post = Post(
        author_id="u1",
        content="Первый тестовый пост"
    )

    db.add_all([user, hobby, post])
    db.commit()