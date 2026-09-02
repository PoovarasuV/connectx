from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import Profile, User
from app.schemas.profile import (
    ProfileCreateRequest,
    ProfileResponse,
    ProfileUpdateRequest,
)


router = APIRouter(
    prefix="/users/me",
    tags=["Profile"],
)


@router.post(
    "/profile",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    request: ProfileCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing_profile = db.scalar(
        select(Profile).where(
            Profile.user_id == current_user.id
        )
    )

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile already exists.",
        )

    existing_username = db.scalar(
        select(Profile).where(
            Profile.username == request.username
        )
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken.",
        )

    profile = Profile(
        user_id=current_user.id,
        username=request.username,
        display_name=request.display_name,
        bio=request.bio,
        avatar_url=request.avatar_url,
        location=request.location,
        latitude=request.latitude,
        longitude=request.longitude,
        date_of_birth=request.date_of_birth,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.get(
    "/profile",
    response_model=ProfileResponse,
)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.scalar(
        select(Profile).where(
            Profile.user_id == current_user.id
        )
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )

    return profile


@router.put(
    "/profile",
    response_model=ProfileResponse,
)
def update_profile(
    request: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.scalar(
        select(Profile).where(
            Profile.user_id == current_user.id
        )
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )

    if request.username is not None:
        existing_username = db.scalar(
            select(Profile).where(
                Profile.username == request.username,
                Profile.user_id != current_user.id,
            )
        )

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username is already taken.",
            )

        profile.username = request.username

    if request.display_name is not None:
        profile.display_name = request.display_name

    if request.bio is not None:
        profile.bio = request.bio

    if request.avatar_url is not None:
        profile.avatar_url = request.avatar_url

    if request.location is not None:
        profile.location = request.location

    if request.latitude is not None:
        profile.latitude = request.latitude

    if request.longitude is not None:
        profile.longitude = request.longitude

    if request.date_of_birth is not None:
        profile.date_of_birth = request.date_of_birth

    db.commit()
    db.refresh(profile)

    return profile


