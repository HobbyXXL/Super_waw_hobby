"""add_likes_table

Revision ID: b49a8b0c98ff
Revises: f7b1b364464f
Create Date: 2026-03-25 15:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b49a8b0c98ff'
down_revision: Union[str, None] = 'f7b1b364464f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'likes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('portfolio_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolio_works.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'portfolio_id', name='unique_user_portfolio_like')
    )
    op.create_index(op.f('ix_likes_id'), 'likes', ['id'], unique=False)
    op.create_index(op.f('ix_likes_user_id'), 'likes', ['user_id'], unique=False)
    op.create_index(op.f('ix_likes_portfolio_id'), 'likes', ['portfolio_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_likes_portfolio_id'), table_name='likes')
    op.drop_index(op.f('ix_likes_user_id'), table_name='likes')
    op.drop_index(op.f('ix_likes_id'), table_name='likes')
    op.drop_table('likes')