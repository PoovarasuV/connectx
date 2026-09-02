from pydantic import BaseModel, Field, model_validator


class UserPreferenceCreateRequest(BaseModel):
    min_age: int = Field(
        ge=18,
        le=100,
    )

    max_age: int = Field(
        ge=18,
        le=100,
    )

    preferred_distance_km: int = Field(
        ge=1,
        le=500,
        default=10,
    )

    @model_validator(mode="after")
    def validate_age_range(self):
        if self.max_age < self.min_age:
            raise ValueError(
                "max_age must be greater than or equal to min_age."
            )

        return self


class UserPreferenceResponse(BaseModel):
    id: str
    user_id: str
    min_age: int
    max_age: int
    preferred_distance_km: int

    model_config = {
        "from_attributes": True,
    }
