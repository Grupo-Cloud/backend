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


@router.get("/me", response_model=GetUserDetail)
def get_user_from_token(user: Annotated[User, Depends(get_user)]):
    return user
