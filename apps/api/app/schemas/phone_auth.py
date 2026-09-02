from pydantic import BaseModel, Field


class RequestOTPRequest(BaseModel):
    phone_number: str = Field(
        min_length=10,
        max_length=20,
    )


class RequestOTPResponse(BaseModel):
    message: str


class VerifyOTPRequest(BaseModel):
    phone_number: str = Field(
        min_length=10,
        max_length=20,
    )
    otp: str = Field(
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$",
    )


class VerifyOTPResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    phone_number: str
