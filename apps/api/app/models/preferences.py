from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    min_age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    max_age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    preferred_distance_km: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("10"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    user: Mapped["User"] = relationship()

    __table_args__ = (
        CheckConstraint(
            "min_age >= 18",
            name="ck_user_preferences_min_age",
        ),
        CheckConstraint(
            "max_age >= min_age",
            name="ck_user_preferences_age_range",
        ),
        CheckConstraint(
            "preferred_distance_km > 0",
            name="ck_user_preferences_distance",
        ),
    )
