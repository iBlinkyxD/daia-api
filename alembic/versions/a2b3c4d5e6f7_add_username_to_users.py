"""add username to users

Revision ID: a2b3c4d5e6f7
Revises: e3c1b0a2f94d
Create Date: 2026-03-25

"""
from typing import Sequence, Union
import re
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session


revision: str = "a2b3c4d5e6f7"
down_revision: Union[str, None] = "e3c1b0a2f94d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def generate_username(first_name: str, last_name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", f"{first_name}{last_name}".lower())


def upgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(), nullable=True))
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    # Backfill existing users
    bind = op.get_bind()
    session = Session(bind=bind)

    rows = session.execute(sa.text("SELECT id, first_name, last_name FROM users")).fetchall()
    used: set[str] = set()

    for row in rows:
        base = generate_username(row.first_name, row.last_name)
        username = base
        counter = 2
        while username in used:
            username = f"{base}{counter}"
            counter += 1
        used.add(username)
        session.execute(
            sa.text("UPDATE users SET username = :username WHERE id = :id"),
            {"username": username, "id": row.id},
        )

    session.commit()


def downgrade() -> None:
    op.drop_index("ix_users_username", table_name="users")
    op.drop_column("users", "username")