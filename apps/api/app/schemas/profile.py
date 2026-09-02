from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class ProfileCreateRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )

    display_name: str = Field(
        min_length=1,
        max_length=100,
    )

    bio: str | None = Field(
        default=None,
        max_length=500,
    )

    avatar_url: str | None = None

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    latitude: float | None = None

    longitude: float | None = None

    date_of_birth: date | None = None


class ProfileUpdateRequest(BaseModel):
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
    )

    display_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    bio: str | None = Field(
        default=None,
        max_length=500,
    )

    avatar_url: str | None = None

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    latitude: float | None = None

    longitude: float | None = None

    date_of_birth: date | None = None


class ProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    username: str
    display_name: str
    bio: str | None
    avatar_url: str | None
    location: str | None
    latitude: float | None
    longitude: float | None
    date_of_birth: date | None

    model_config = {
        "from_attributes": True,
    }


