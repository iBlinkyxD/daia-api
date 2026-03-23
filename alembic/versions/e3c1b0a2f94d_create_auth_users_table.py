"""create auth_users for User API (separate from Academy users)

Revision ID: e3c1b0a2f94d
Revises:
Create Date: 2026-03-22

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e3c1b0a2f94d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "auth_users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("profile_picture_url", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("verification_code", sa.String(), nullable=True),
        sa.Column("verification_expires", sa.DateTime(), nullable=True),
        sa.Column("pending_email", sa.String(), nullable=True),
        sa.Column("email_verification_code", sa.String(), nullable=True),
        sa.Column("email_verification_expires", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_auth_users_id"), "auth_users", ["id"], unique=False)
    op.create_index(op.f("ix_auth_users_email"), "auth_users", ["email"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_auth_users_email"), table_name="auth_users")
    op.drop_index(op.f("ix_auth_users_id"), table_name="auth_users")
    op.drop_table("auth_users")
