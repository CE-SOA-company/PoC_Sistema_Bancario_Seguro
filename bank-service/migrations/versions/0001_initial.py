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
        "accounts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("account_id", sa.String(length=100), nullable=False, unique=True),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("balance", sa.Float(), nullable=False),
        sa.Column("required_integrity_level", sa.Integer(), nullable=False),
    )
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("transaction_id", sa.String(length=100), nullable=False, unique=True),
        sa.Column("account_id", sa.String(length=100), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("actor_integrity_level", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.String(length=100), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("transactions")
    op.drop_table("accounts")
