from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    Boolean,
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


class Connection(Base):
    __tablename__ = "connections"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    connected_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )

    connected_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[connected_user_id],
    )

    __table_args__ = (
        Index("idx_connections_connected_user_id", "connected_user_id"),
        CheckConstraint(
            "user_id <> connected_user_id",
            name="chk_connections_different_users",
        ),
        CheckConstraint(
            "user_id < connected_user_id",
            name="chk_connections_order",
        ),
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    sender_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    receiver_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    sender: Mapped["User"] = relationship(
        "User",
        foreign_keys=[sender_id],
    )

    receiver: Mapped["User"] = relationship(
        "User",
        foreign_keys=[receiver_id],
    )

    __table_args__ = (
        Index("idx_messages_created_at", "created_at"),
        Index("idx_messages_receiver_id", "receiver_id"),
        Index("idx_messages_sender_id", "sender_id"),
        CheckConstraint(
            "sender_id <> receiver_id",
            name="chk_messages_different_users",
        ),
    )


class Notification(Base):
    __tablename__ = "notifications"

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
    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
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
        Index("idx_notifications_is_read", "is_read"),
        Index("idx_notifications_user_id", "user_id"),
    )
