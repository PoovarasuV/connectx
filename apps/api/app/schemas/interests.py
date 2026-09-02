from uuid import UUID

from pydantic import BaseModel, Field


class InterestCreateRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )

    category: str | None = Field(
        default=None,
        max_length=100,
    )


class InterestResponse(BaseModel):
    id: UUID
    name: str
    category: str | None

    model_config = {
        "from_attributes": True,
    }


class UserInterestsUpdateRequest(BaseModel):
    interest_ids: list[UUID] = Field(
        min_length=1,
        max_length=20,
    )


class UserInterestsResponse(BaseModel):
    interests: list[InterestResponse]
