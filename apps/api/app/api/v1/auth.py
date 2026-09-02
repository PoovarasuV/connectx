from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.db.database import get_db
from app.models.revoked_token import RevokedToken
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

security = HTTPBearer()


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing_user = db.scalar(
        select(User).where(User.email == request.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        )

    user = User(
        email=request.email,
        password_hash=hash_password(request.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return RegisterResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
    )


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.scalar(
        select(User).where(User.email == request.email)
    )

    if not user or not verify_password(
        request.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(str(user.id))

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        user_id = payload.get("sub")
        token_jti = payload.get("jti")
        expires_at_timestamp = payload.get("exp")

        if (
            user_id is None
            or token_jti is None
            or expires_at_timestamp is None
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token.",
            )

        expires_at = datetime.fromtimestamp(
            expires_at_timestamp,
            tz=timezone.utc,
        )

    except (JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
        )

    existing_revocation = db.scalar(
        select(RevokedToken).where(
            RevokedToken.jti == token_jti
        )
    )

    if existing_revocation is None:
        revoked_token = RevokedToken(
            jti=token_jti,
            user_id=user_id,
            expires_at=expires_at,
        )

        db.add(revoked_token)
        db.commit()

    return None


