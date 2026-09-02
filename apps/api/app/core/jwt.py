from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import HTTPException, status

from jose import JWTError, jwt

from app.config import settings


def create_access_token(user_id: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": user_id,
        "jti": str(uuid4()),
        "exp": expires_at,
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def verify_access_token(token: str) -> tuple[str, str]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        user_id = payload.get("sub")
        token_type = payload.get("type")
        token_jti = payload.get("jti")

        if (
            user_id is None
            or token_type != "access"
            or token_jti is None
        ):
            raise credentials_exception

        return user_id, token_jti

    except JWTError:
        raise credentials_exception

