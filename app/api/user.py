from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_user
from app.models.user import User
from app.schemas.user import GetUserDetail


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"detail": "Could not find the requested user"}},
)


@router.get("/{user_id}", response_model=GetUserDetail)
def get_user_from_id(user_id: UUID, user: Annotated[User, Depends(get_user)]):
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )
    return user
