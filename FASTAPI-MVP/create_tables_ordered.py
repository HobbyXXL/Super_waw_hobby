from database import engine
from models import Base

# Явный порядок: сначала таблицы без FK, потом с FK
ordered_tables = [
    "users",        # сначала пользователи
    "hobbies",      # хобби без зависимостей
    "goals",
    "levels",
    "materials",
    "tags",         # теги без зависимостей
    "posts",        # посты ссылаются на users
    "post_tags",    # связь post-tag
    "likes",        # лайки на posts
    "comments",     # комментарии на posts
    "reposts",      # репосты на posts
    # добавь остальные свои таблицы в правильном порядке
]

for table_name in ordered_tables:
    if table_name in Base.metadata.tables:
        Base.metadata.tables[table_name].create(bind=engine, checkfirst=True)

print("Таблицы созданы в правильном порядке")