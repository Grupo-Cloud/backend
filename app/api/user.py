from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_user
from app.exceptions.user import UserNotFoundException
from app.models.user import User
from app.schemas.user import GetUserDetail
from app.schemas.chat import GetChatDetail
from app.schemas.document import GetDocumentDetail

from app.services.user import service


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"detail": "Could not find the requested user"}},
)


@router.get("/me", response_model=GetUserDetail)
def get_current_user(user: Annotated[User, Depends(get_user)]):
    return user


@router.get("/{user_id}/documents", response_model=list[GetDocumentDetail])
def get_user_documents(
    user_id: UUID,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )
    try:
        return service.get_documents_from_user(db, user_id)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find the user you are trying to get documents from",
        )


@router.get("/{user_id}/chats", response_model=list[GetChatDetail])
def get_user_chats(
    user_id: UUID,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )
    try:
        return service.get_chats_from_user(db, user_id)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find the user you are trying to get chats from",
        )
