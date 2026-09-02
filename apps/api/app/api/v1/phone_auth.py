from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.db.database import get_db
from app.models.user import User
from app.schemas.phone_auth import (
    RequestOTPRequest,
    RequestOTPResponse,
    VerifyOTPRequest,
    VerifyOTPResponse,
)
from app.services.otp import create_otp, verify_otp_for_phone


router = APIRouter(
    prefix="/auth/phone",
    tags=["Phone Authentication"],
)


@router.post(
    "/request-otp",
    response_model=RequestOTPResponse,
)
def request_otp(
    request: RequestOTPRequest,
    db: Session = Depends(get_db),
):
    otp = create_otp(
        db=db,
        phone_number=request.phone_number,
    )

    return RequestOTPResponse(
        message=f"OTP generated successfully. Development OTP: {otp}",
    )


@router.post(
    "/verify-otp",
    response_model=VerifyOTPResponse,
)
def verify_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db),
):
    is_valid = verify_otp_for_phone(
        db=db,
        phone_number=request.phone_number,
        otp=request.otp,
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP.",
        )

    user = db.scalar(
        select(User).where(User.phone == request.phone_number)
    )

    if user is None:
        user = User(
            phone=request.phone_number,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    access_token = create_access_token(str(user.id))

    return VerifyOTPResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user.id),
        phone_number=user.phone,
    )
