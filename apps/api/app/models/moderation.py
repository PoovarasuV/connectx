from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    reporter_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    reported_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    reason: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default=text("'pending'"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    reporter: Mapped["User"] = relationship(
        "User",
        foreign_keys=[reporter_id],
    )

    reported_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[reported_user_id],
    )

    __table_args__ = (
        Index("idx_reports_reported_user_id", "reported_user_id"),
        Index("idx_reports_reporter_id", "reporter_id"),
        Index("idx_reports_status", "status"),
        CheckConstraint(
            "reporter_id <> reported_user_id",
            name="chk_reports_different_users",
        ),
    )


class Block(Base):
    __tablename__ = "blocks"

    blocker_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    blocked_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    blocker: Mapped["User"] = relationship(
        "User",
        foreign_keys=[blocker_id],
    )

    blocked_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[blocked_user_id],
    )

    __table_args__ = (
        Index("idx_blocks_blocked_user_id", "blocked_user_id"),
        CheckConstraint(
            "blocker_id <> blocked_user_id",
            name="chk_blocks_different_users",
        ),
    )
