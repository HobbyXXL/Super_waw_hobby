# Добавляет временные поля temp_login, temp_password_hash и temp_role в таблицу email_verifications для хранения данных регистрации до подтверждения email.
"""add_last_seen_to_users

Revision ID: f7b1b364464f
Revises: 47e97064537a
Create Date: 2026-03-24 13:53:05.937250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f7b1b364464f'
down_revision: Union[str, Sequence[str], None] = '47e97064537a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'last_seen')
