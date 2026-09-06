"""add watchlist updated_at

Revision ID: c4e8f1a2b9d0
Revises: a66f6aefe236
Create Date: 2026-09-06 13:47:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c4e8f1a2b9d0"
down_revision: Union[str, Sequence[str], None] = "a66f6aefe236"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("watchlist_table", sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.execute("UPDATE watchlist_table SET updated_at = created_at WHERE updated_at IS NULL")
    op.alter_column("watchlist_table", "updated_at", nullable=False)


def downgrade() -> None:
    op.drop_column("watchlist_table", "updated_at")
