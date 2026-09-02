from datetime import date, datetime
from uuid import UUID

from sqlalchemy import (
    Date,
    DateTime,
    Double,
    ForeignKey,
    Index,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
    phone: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
    )
    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        server_default=text("true"),
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

    profile: Mapped["Profile | None"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    bio: Mapped[str | None] = mapped_column(Text)
    avatar_url: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(255))
    latitude: Mapped[float | None] = mapped_column(Double)
    longitude: Mapped[float | None] = mapped_column(Double)
    date_of_birth: Mapped[date | None] = mapped_column(Date)
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

    user: Mapped["User"] = relationship(back_populates="profile")


class Interest(Base):
    __tablename__ = "interests"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    category: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )


class UserInterest(Base):
    __tablename__ = "user_interests"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    interest_id: Mapped[UUID] = mapped_column(
        ForeignKey("interests.id", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    __table_args__ = (
        Index("idx_user_interests_interest_id", "interest_id"),
    )
