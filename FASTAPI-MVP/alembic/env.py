# alembic/env.py

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 1. Добавляем корень проекта в sys.path (это решает проблему импортов)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# 2. Загружаем .env
from dotenv import load_dotenv
load_dotenv()

# 3. Импортируем модели напрямую из корня (без api/ или app/)
from models import Base
from models.user import User
from models.hobby import Hobby

# Раскомментируй, когда создашь эти файлы
# from models.post import Post
# from models.like import Like
# from models.comment import Comment
# from models.repost import Repost
# from models.tag import Tag

# 4. Конфиг alembic
config = context.config

# 5. Берём DATABASE_URL из .env
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)
else:
    print("ВНИМАНИЕ: DATABASE_URL не найден в .env — используется значение из alembic.ini")

# 6. Логи
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 7. Метаданные моделей
target_metadata = Base.metadata

# 8. Функции миграций (оставляем стандартные)
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()