from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    reference_id: Mapped[UUID | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )

    __table_args__ = (
        Index("idx_activities_created_at", "created_at"),
        Index("idx_activities_user_id", "user_id"),
    )


class Reputation(Base):
    __tablename__ = "reputation"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    score: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        server_default=text("0.00"),
    )
    completed_activities: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )
    positive_interactions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )
    negative_interactions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )

    __table_args__ = (
        CheckConstraint(
            "score >= 0",
            name="chk_reputation_score",
        ),
        CheckConstraint(
            "completed_activities >= 0",
            name="chk_reputation_completed",
        ),
        CheckConstraint(
            "positive_interactions >= 0",
            name="chk_reputation_positive",
        ),
        CheckConstraint(
            "negative_interactions >= 0",
            name="chk_reputation_negative",
        ),
    )
