from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text)
    creator_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    avatar_url: Mapped[str | None] = mapped_column(Text)
    visibility: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default=text("'public'"),
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

    members: Mapped[list["GroupMember"]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("idx_groups_creator_id", "creator_id"),
    )


class GroupMember(Base):
    __tablename__ = "group_members"

    group_id: Mapped[UUID] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default=text("'member'"),
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    group: Mapped["Group"] = relationship(
        back_populates="members"
    )

    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )

    __table_args__ = (
        Index("idx_group_members_user_id", "user_id"),
    )
