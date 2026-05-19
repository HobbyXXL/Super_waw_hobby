# Добавляет временные поля temp_login, temp_password_hash и temp_role в таблицу email_verifications для хранения данных регистрации до подтверждения email.
"""add_temp_fields_to_email_verification

Revision ID: dbf925ed0898
Revises: c588da365e0d
Create Date: 2026-04-21 18:56:54.423479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'dbf925ed0898'
down_revision: Union[str, Sequence[str], None] = 'c588da365e0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('email_verifications', sa.Column('temp_login', sa.String(), nullable=True))
    op.add_column('email_verifications', sa.Column('temp_password_hash', sa.String(), nullable=True))
    op.add_column('email_verifications', sa.Column('temp_role', sa.String(), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('email_verifications', 'temp_role')
    op.drop_column('email_verifications', 'temp_password_hash')
    op.drop_column('email_verifications', 'temp_login')
