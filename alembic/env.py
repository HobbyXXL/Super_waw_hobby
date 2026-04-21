from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from models.base import Base

# Импортируем ВСЕ модели, чтобы Alembic их "увидел"
import models.terms_versions
import models.users
import models.user_profiles
import models.hobbies
import models.goals
import models.levels
import models.materials
import models.user_hobbies
import models.user_goals
import models.portfolio_works
import models.user_activity
import models.chats
import models.messages

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    from database import engine
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
