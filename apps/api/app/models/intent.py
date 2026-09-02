from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Double,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Intent(Base):
    __tablename__ = "intents"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    creator_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text)
    intent_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    location: Mapped[str | None] = mapped_column(String(255))
    latitude: Mapped[float | None] = mapped_column(Double)
    longitude: Mapped[float | None] = mapped_column(Double)
    start_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    max_participants: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default=text("'active'"),
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

    creator: Mapped["User"] = relationship(
        "User",
        foreign_keys=[creator_id],
    )

    participants: Mapped[list["IntentParticipant"]] = relationship(
        back_populates="intent",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("idx_intents_creator_id", "creator_id"),
        Index("idx_intents_status", "status"),
        Index("idx_intents_start_time", "start_time"),
        CheckConstraint(
            "max_participants IS NULL OR max_participants > 0",
            name="chk_intents_participants",
        ),
        CheckConstraint(
            "end_time IS NULL OR start_time IS NULL OR end_time > start_time",
            name="chk_intents_time",
        ),
    )


class IntentParticipant(Base):
    __tablename__ = "intent_participants"

    intent_id: Mapped[UUID] = mapped_column(
        ForeignKey("intents.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default=text("'accepted'"),
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    intent: Mapped["Intent"] = relationship(
        back_populates="participants"
    )

    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )

    __table_args__ = (
        Index("idx_intent_participants_user_id", "user_id"),
    )
