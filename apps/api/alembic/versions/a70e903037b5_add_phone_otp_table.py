"""add phone otp table

Revision ID: a70e903037b5
Revises: b4e52ebb439c
Create Date: 2026-09-02 15:32:22.773866
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.

revision: str = "a70e903037b5"
down_revision: Union[str, Sequence[str], None] = "b4e52ebb439c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the phone OTP table."""

    op.create_table(
        "phone_otps",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "phone_number",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "otp_hash",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "attempts",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "max_attempts",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("5"),
        ),
        sa.Column(
            "is_used",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_phone_otps_phone_number",
        "phone_otps",
        ["phone_number"],
        unique=False,
    )


def downgrade() -> None:
    """Remove the phone OTP table."""

    op.drop_index(
        "ix_phone_otps_phone_number",
        table_name="phone_otps",
    )

    op.drop_table("phone_otps")

