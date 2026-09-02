"""add user preferences

Revision ID: acb5f2584d0a

Revises: b57c8786ac55

Create Date: 2026-09-02 17:33:11.444339

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = "acb5f2584d0a"

down_revision: Union[str, Sequence[str], None] = "b57c8786ac55"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "user_preferences",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "min_age",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "max_age",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "preferred_distance_km",
            sa.Integer(),
            server_default=sa.text("10"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "max_age >= min_age",
            name="ck_user_preferences_age_range",
        ),
        sa.CheckConstraint(
            "min_age >= 18",
            name="ck_user_preferences_min_age",
        ),
        sa.CheckConstraint(
            "preferred_distance_km > 0",
            name="ck_user_preferences_distance",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("user_preferences")
