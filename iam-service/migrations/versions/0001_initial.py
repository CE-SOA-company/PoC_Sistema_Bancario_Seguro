"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-06-15 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(length=100), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("clearance_level", sa.Integer(), nullable=False),
        sa.Column("integrity_level", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
