"""add_activity_status_to_portfolio

Revision ID: 5b12904a2a83
Revises: b49a8b0c98ff
Create Date: 2026-03-25 16:18:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b12904a2a83'
down_revision: Union[str, None] = 'b49a8b0c98ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('portfolio_works', sa.Column('activity_status', sa.String(), nullable=True))
    # Устанавливаем дефолтное значение для существующих записей
    op.execute("UPDATE portfolio_works SET activity_status = 'did_hobby' WHERE activity_status IS NULL")
    # Делаем поле NOT NULL после установки дефолтных значений
    op.alter_column('portfolio_works', 'activity_status', nullable=False, server_default='did_hobby')


def downgrade() -> None:
    op.drop_column('portfolio_works', 'activity_status')