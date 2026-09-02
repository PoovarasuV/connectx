from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.preferences import UserPreference
from app.models.user import User
from app.schemas.preferences import (
    UserPreferenceCreateRequest,
    UserPreferenceResponse,
)


router = APIRouter(
    prefix="/users/me",
    tags=["Preferences"],
)


@router.post(
    "/preferences",
    response_model=UserPreferenceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_preferences(
    request: UserPreferenceCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing_preferences = db.scalar(
        select(UserPreference).where(
            UserPreference.user_id == current_user.id
        )
    )

    if existing_preferences:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Preferences already exist.",
        )

    preferences = UserPreference(
        user_id=current_user.id,
        min_age=request.min_age,
        max_age=request.max_age,
        preferred_distance_km=request.preferred_distance_km,
    )

    db.add(preferences)
    db.commit()
    db.refresh(preferences)

    return preferences
