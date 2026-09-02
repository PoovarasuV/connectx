"""allow phone only users

Revision ID: b57c8786ac55
Revises: a70e903037b5
Create Date: 2026-09-02
"""

from typing import Sequence, Union

from alembic import op


revision: str = "b57c8786ac55"
down_revision: Union[str, Sequence[str], None] = "a70e903037b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "email",
        nullable=True,
    )

    op.alter_column(
        "users",
        "password_hash",
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "password_hash",
        nullable=False,
    )

    op.alter_column(
        "users",
        "email",
        nullable=False,
    )
