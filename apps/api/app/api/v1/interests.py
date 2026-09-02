from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import Interest, User, UserInterest
from app.schemas.interests import (
    InterestCreateRequest,
    InterestResponse,
    UserInterestsResponse,
    UserInterestsUpdateRequest,
)


router = APIRouter(
    tags=["Interests"],
)


@router.post(
    "/interests",
    response_model=InterestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interest(
    request: InterestCreateRequest,
    db: Session = Depends(get_db),
):
    existing_interest = db.scalar(
        select(Interest).where(
            Interest.name == request.name
        )
    )

    if existing_interest:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Interest already exists.",
        )

    interest = Interest(
        name=request.name,
        category=request.category,
    )

    db.add(interest)
    db.commit()
    db.refresh(interest)

    return interest


@router.get(
    "/interests",
    response_model=list[InterestResponse],
)
def list_interests(
    db: Session = Depends(get_db),
):
    interests = db.scalars(
        select(Interest).order_by(Interest.name)
    ).all()

    return interests


@router.put(
    "/users/me/interests",
    response_model=UserInterestsResponse,
)
def update_user_interests(
    request: UserInterestsUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    unique_interest_ids = list(
        dict.fromkeys(request.interest_ids)
    )

    interests = db.scalars(
        select(Interest).where(
            Interest.id.in_(unique_interest_ids)
        )
    ).all()

    if len(interests) != len(unique_interest_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more interests were not found.",
        )

    db.query(UserInterest).filter(
        UserInterest.user_id == current_user.id
    ).delete(
        synchronize_session=False
    )

    for interest_id in unique_interest_ids:
        db.add(
            UserInterest(
                user_id=current_user.id,
                interest_id=interest_id,
            )
        )

    db.commit()

    return UserInterestsResponse(
        interests=interests
    )


@router.get(
    "/users/me/interests",
    response_model=UserInterestsResponse,
)
def get_user_interests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interests = db.scalars(
        select(Interest)
        .join(
            UserInterest,
            UserInterest.interest_id == Interest.id,
        )
        .where(
            UserInterest.user_id == current_user.id
        )
        .order_by(Interest.name)
    ).all()

    return UserInterestsResponse(
        interests=interests
    )
