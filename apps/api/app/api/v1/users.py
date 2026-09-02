from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "phone": current_user.phone,
        "is_active": current_user.is_active,
    }


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.get(User, current_user.id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found.",
        )

    db.delete(user)
    db.commit()

    return None

